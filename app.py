from flask import Flask, render_template
from flask_socketio import SocketIO, send
import requests
import os
import base64
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
socketio = SocketIO(app)

SPOTIFY_API_URL = 'https://api.spotify.com/v1/recommendations'
SPOTIFY_PLAYLISTS_URL = 'https://api.spotify.com/v1/search'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

@app.route('/')
def home():
    return render_template('chat.html')

@socketio.on('message')
def handle_message(msg):
    send(f"User: {msg}", broadcast=True)
    print(f"Received message: {msg}")

    greeting_response = check_for_greeting(msg)
    if greeting_response:
        send(f"Bot: {greeting_response}", broadcast=True)
        return

    genre, mood = extract_genre_and_mood(msg)
    print(f"Extracted genre: {genre}, mood: {mood}")

    if genre or mood:
        access_token = get_spotify_access_token()
        if not access_token:
            send("Bot: Error fetching Spotify access token.", broadcast=True)
            return

        spotify_recommendations = []
        headers = {'Authorization': f'Bearer {access_token}'}
        params = {'seed_genres': genre or 'pop', 'limit': 5}
        response = requests.get(SPOTIFY_API_URL, headers=headers, params=params)

        if response.status_code == 200:
            recommendations = response.json().get('tracks', [])
            spotify_recommendations = [(track['name'], track['external_urls']['spotify']) for track in recommendations]
        else:
            print(f"Spotify API error: {response.status_code}, {response.text}")
            send("Bot: Error fetching recommendations from Spotify.", broadcast=True)

        playlists = fetch_playlists(genre, mood, access_token)

        if spotify_recommendations or playlists:
            message = f"Here are some {genre or mood} recommendations:<br>From Spotify:<br>"
            for track, url in spotify_recommendations:
                message += f"<a href='{url}' target='_blank'>{track}</a><br>"
            if playlists:
                message += "<br>Playlists you might enjoy:<br>"
                for playlist_name, playlist_url in playlists:
                    message += f"<a href='{playlist_url}' target='_blank'>{playlist_name}</a><br>"
            send(f"Bot: {message}", broadcast=True)
        else:
            send(f"Bot: Sorry, I couldn't find any recommendations for {genre or mood}.", broadcast=True)
    else:
        send("Bot: Sorry, I can only provide recommendations for specific genres like pop, rock, classical, or moods like happy, sad, etc.", broadcast=True)

def check_for_greeting(user_input):
    greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']
    for greeting in greetings:
        if greeting in user_input.lower():
            return "Hello! How can I help you today?"
    return None

def extract_genre_and_mood(user_input):
    genres = ['pop', 'rock', 'hip-hop', 'rap', 'jazz', 'classical',
              'electronic', 'country', 'reggae', 'blues', 'r&b',
              'soul', 'metal', 'folk', 'punk', 'indie', 'latin',
              'alternative', 'k-pop']
    moods = ['happy', 'sad', 'chill', 'romantic', 'energetic', 'calm', 'party', 'focus']

    detected_genre = next((genre for genre in genres if genre in user_input.lower()), None)
    detected_mood = next((mood for mood in moods if mood in user_input.lower()), None)

    return detected_genre, detected_mood

def get_spotify_access_token():
    auth_header = base64.b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()).decode()
    headers = {'Authorization': f'Basic {auth_header}'}
    data = {'grant_type': 'client_credentials'}

    response = requests.post(TOKEN_URL, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(f"Failed to get Spotify token: {response.status_code}, {response.text}")
        return None

def fetch_playlists(genre, mood, access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    query = genre if genre else mood
    params = {'q': query, 'type': 'playlist', 'limit': 5}
    response = requests.get(SPOTIFY_PLAYLISTS_URL, headers=headers, params=params)

    if response.status_code == 200:
        playlists = response.json().get('playlists', {}).get('items', [])
        return [(playlist['name'], playlist['external_urls']['spotify']) for playlist in playlists]
    else:
        print(f"Failed to fetch playlists: {response.status_code}, {response.text}")
        return []


if __name__ == '__main__':
    socketio.run(app, debug=True, port=8000)

