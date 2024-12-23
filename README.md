# Beat Bot 🎵🤖

**Beat Bot** is an AI-powered chatbot that curates music recommendations based on your mood and genre preferences. With Spotify API integration, it delivers personalized song suggestions and playlists in real-time, making music discovery effortless and interactive.

---

## Features

- **Mood-Based Recommendations**: Tailored song suggestions to match your mood.
- **Genre-Specific Suggestions**: Recommendations across genres like pop, jazz, rock, classical, and more.
- **Spotify Integration**: Fetches playlists and tracks directly from Spotify’s extensive music library.
- **Responsive Chat Interface**: Interactive design optimized for both desktop and mobile users.

---

## Technologies Used

- **Backend**: Flask (Python)
- **Chat Interface**: Socket.IO
- **API Integration**: Spotify API
- **Frontend**: HTML, CSS, JavaScript

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/raina1806/Beat-Bot.git
    cd Beat-Bot
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up Spotify API credentials:
    - Create a Spotify developer account and obtain your `Client ID` and `Client Secret`.
    - Add them to `app.py`:
      ```python
      SPOTIFY_CLIENT_ID = 'your_client_id'
      SPOTIFY_CLIENT_SECRET = 'your_client_secret'
      ```

4. Run the Flask server:
    ```bash
    python app.py
    ```

5. Open your browser and navigate to `http://127.0.0.1:5000/` to start chatting with Beat Bot.

---

## Project Structure

beat-bot/ 
├── templates/ 
│ └── chat.html
│ └── index.html
├── static/ 
│ └── style.css 
│ └── style-desktop.css 
│ └── style-mobile.css 
├── app.py 
├── requirements.txt 
├── README.md


### Chat Interface
![Chat Interface](https://example.com/chat-interface.png)

---

## Future Enhancements

- Advanced NLP for more accurate mood detection.
- Integration with additional streaming platforms like YouTube Music or Apple Music.
- User profiles for personalized music histories.
- Dynamic AI-driven playlist generation based on listening trends.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to help improve Beat Bot.

---

**Beat Bot** – Your AI-powered music discovery assistant for personalized listening experiences.
