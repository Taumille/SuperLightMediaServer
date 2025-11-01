from flask import Flask, render_template, redirect, url_for, session, request, flash, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from user_agents import parse
import sqlite3
import os
import env
import time

app = Flask(__name__)
app.secret_key = env.SECRET_FLASK_KEY
password_hashed = env.PASSWORD

def get_movies():
    """Fetch all movies from the database."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM movies ORDER BY name ASC")
    movies = cursor.fetchall()
    conn.close()
    return movies


def get_series():
    """Fetch all movies from the database."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT series_name FROM series ORDER BY series_name ASC")
    movies = cursor.fetchall()
    series = [mov[0] for mov in movies]
    conn.close()
    return series


@app.route('/series/<series_name>')
def series_detail(series_name):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    # Fetch the series description and episodes
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    # Get series description (assuming you have a 'description' column)
    cursor.execute("SELECT description FROM series WHERE series_name = ? LIMIT 1", (series_name,))
    description = cursor.fetchone()

    # Get all episodes for the series
    cursor.execute("""
        SELECT id, series_name, path, episode
        FROM series
        WHERE series_name = ?
        ORDER BY episode ASC
    """, (series_name,))
    episodes = cursor.fetchall()
    print(episodes)

    conn.close()

    return render_template('series_detail.html', series_name=series_name, description=description, episodes=episodes)


@app.route('/media/<path:id>')
def media_file(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("SELECT path FROM movies WHERE id = ?", (id,))
    result = cursor.fetchone()
    conn.close()
    print(result)

    file_id = os.path.basename(result[0])
    link_path = env.WEB_SERVER_PATH + file_id
    try:
        os.symlink(result[0], link_path)
    except FileExistsError:
        os.utime(link_path, (time.time(), time.time()),
                 follow_symlinks=False)

    user_agent_string = request.headers.get('User-Agent', '')
    is_linux = 'Linux' in user_agent_string
    if not is_linux:
        # Create an m3u
        with open(env.WEB_SERVER_PATH + file_id + ".m3u", "w") as f:
            f.write(env.WEB_SERVER_LINK+file_id)
        return send_file(env.WEB_SERVER_PATH+file_id+".m3u")
    return redirect("vlc://" + env.WEB_SERVER_LINK+file_id)



@app.route('/series_media/<path:id>')
def series_file(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("SELECT path FROM series WHERE id = ?", (id,))
    result = cursor.fetchone()
    conn.close()
    print(result)

    file_id = os.path.basename(result[0])
    link_path = env.WEB_SERVER_PATH + file_id
    try:
        os.symlink(result[0], link_path)
    except FileExistsError:
        os.utime(link_path, (time.time(), time.time()),
                 follow_symlinks=False)

    user_agent_string = request.headers.get('User-Agent', '')
    is_linux = 'Linux' in user_agent_string
    if not is_linux:
        # Create an m3u
        with open(env.WEB_SERVER_PATH + file_id + ".m3u", "w") as f:
            f.write(env.WEB_SERVER_LINK+file_id)
        return send_file(env.WEB_SERVER_PATH+file_id+".m3u")
    return redirect("vlc://" + env.WEB_SERVER_LINK+file_id)


@app.route("/service")
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template("index.html")


@app.route("/movies")
def movies():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    movies = get_movies()
    return render_template("movies.html", movies=movies)


@app.route("/series")
def series():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    movies = get_series()
    return render_template("series.html", movies=movies)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if check_password_hash(password_hashed, password):
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Incorrect password. Please try again.', 'error')
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
