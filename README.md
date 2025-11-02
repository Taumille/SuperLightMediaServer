# 🎬 SuperLight Media Server

A lightweight **Flask-based media library** for organizing, browsing, and streaming your **movies and TV series**.  
It automatically scans folders, cleans filenames, fetches metadata from TMDb, and serves an elegant web interface to play your media locally via VLC.

---

## 📁 Project Structure

```
.
├── app.py / main.py          # Flask web application
├── cleaner.py                # Filename parser & metadata cleaner
├── mdb.py                    # TMDb API integration & database manager
├── main.py                   # File scanning and automatic database updates
├── env.py                    # Environment variables and configuration
├── static/
│   ├── styles/style.css      # Global styles
│   ├── pictures/             # Movie & series posters
│   └── assets/play.png       # Play button asset
├── templates/
│   ├── index.html            # Home screen
│   ├── login.html            # Login page
│   ├── movies.html           # Movies grid
│   ├── series.html           # Series list
│   └── series_detail.html    # Series episode viewer
└── movies.db                 # SQLite database
```

---

## 🚀 Features

- 🧭 **Automatic media discovery**  
  Scans your `MOVIE_PATH` and `SERIES_PATH` folders for new videos.

- 🧹 **Smart filename cleaning**  
  Removes dates, dots, episode codes, and web tags for cleaner titles.

- 🎞️ **Metadata fetching via TMDb API**  
  Automatically retrieves movie & series information and posters.

- 🔐 **Secure access**  
  Simple login system with hashed passwords (Werkzeug).

- 💾 **SQLite database**  
  Stores movies, series, episodes, and their paths.

- 🖼️ **Responsive web interface**  
  Built with HTML templates and custom CSS.

- 🎧 **VLC streaming integration**  
  Opens media directly in VLC or serves `.m3u` playlists.

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/SuperLightMediaServer.git
cd SuperLightMediaServer
```

### 2️⃣ Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

> Typical dependencies:
> - `flask`
> - `werkzeug`
> - `tmdbv3api`
> - `user-agents`
> - `wget`

### 4️⃣ Configure environment
Edit `env.py` to match your system paths and API keys:

```python
SECRET_API_KEY = "your_tmdb_api_key"
WEB_SERVER_PATH = "/path/to/tmp/webserver/"
WEB_SERVER_LINK = "http://localhost:8000/tmp/"
MOVIE_PATH = "/path/to/Movies"
SERIES_PATH = "/path/to/Series"
PASSWORD = "hashed_password_here"
SECRET_FLASK_KEY = "super_secret_flask_key"
```

To generate a password hash:
```python
from werkzeug.security import generate_password_hash
print(generate_password_hash("yourpassword"))
```

### 5️⃣ Initialize the database
Run the app once to create `movies.db` automatically:
```bash
python3 app.py
```

---

## 🧠 Core Components

### 🧩 `Cleaner` (cleaner.py)
Handles media filename parsing and normalization:
- Removes extensions and site tags
- Extracts release years
- Identifies episodes (`S01E01`)
- Formats titles for database storage

### 🎬 `MovieDB` (mdb.py)
Handles SQLite operations and TMDb lookups:
- Creates and populates `movies` and `series` tables
- Downloads posters from TMDb
- Falls back to default poster on missing metadata

### 🔁 `Main` (main.py)
Automated background process that:
- Periodically removes expired symbolic links
- Scans movie/series directories for new files
- Updates the database using `Cleaner` and `MovieDB`

### 🌐 Flask App (`app.py`)
Provides the web interface and routes:
| Route | Description |
|-------|--------------|
| `/` | Login page |
| `/service` | Dashboard after login |
| `/movies` | Movie gallery |
| `/series` | Series overview |
| `/series/<series_name>` | Series details and episodes |
| `/media/<id>` | Stream a specific movie |
| `/series_media/<id>` | Stream a specific episode |
| `/series_all/<series_name>` | Play all episodes as `.m3u` playlist |

---

## 🖥️ Usage

1. Start the server:
   ```bash
   python3 app.py
   ```

2. Visit [http://localhost:5000](http://localhost:5000)

3. Log in with your configured password (`env.PASSWORD`)

4. Browse and stream your media 🎉

---

## 🧰 Optional Background Scanner

To automatically sync new files, run:
```bash
python3 main.py
```

This will:
- Add new movies and series
- Remove expired links
- Keep the database in sync with your filesystem

---

## 🎨 UI Preview

| Screen | Description |
|--------|--------------|
| 🏠 Home | Choose between Movies and Series |
| 🎞️ Movies | Browse movies with posters |
| 📺 Series | View available series |
| 🎬 Series Detail | View description and play individual episodes |
| 🔑 Login | Secure password-protected access |

---

## 🔒 Security Notes

- Uses `werkzeug.security` for password hashing.
- Flask `session` for authentication state.
- `.env` or `env.py` should **never** be committed with real keys or passwords.

---

## 🧑‍💻 Contributing

1. Fork the repository  
2. Create a feature branch  
   ```bash
   git checkout -b feature/new-feature
   ```
3. Commit changes and push  
   ```bash
   git commit -m "Add new feature"
   git push origin feature/new-feature
   ```
4. Open a pull request 🚀

---

## 🪪 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 💡 Credits

- Built with [Flask](https://flask.palletsprojects.com/)
- Metadata from [TMDb API](https://www.themoviedb.org/documentation/api)
- Styled with custom CSS inspired by **Hack font**
- Developed by **Thomas** 🎥

## TODO

TODO:
- [x] Clean filename
- [x] Get info from TMDB
- [x] Save info to DB
- [x] Integrate in Flask
- [x] Create UI
- [x] Create media player
- [x] Autoremove UUID links after 1d
- [ ] Take count of already watched movies
- [x] Update the database when new medias are added
- [x] Process the series
- [x] Make it work on Windows
