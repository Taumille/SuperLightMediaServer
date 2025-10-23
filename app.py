from flask import Flask, render_template, redirect, url_for
import sqlite3
import os
import uuid
import env

app = Flask(__name__)

def get_movies():
    """Fetch all movies from the database."""
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM movies ORDER BY name ASC")
    movies = cursor.fetchall()
    conn.close()
    return movies


def get_series():
    """Fetch all movies from the database."""
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT series_name FROM series ORDER BY series_name ASC")
    movies = cursor.fetchall()
    series = [mov[0] for mov in movies]
    conn.close()
    return series


@app.route('/series/<series_name>')
def series_detail(series_name):
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

    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("SELECT path FROM movies WHERE id = ?", (id,))
    result = cursor.fetchone()
    conn.close()
    print(result)

    file_id = str(uuid.uuid4())
    link_path = env.WEB_SERVER_PATH + file_id
    os.symlink(result[0], link_path)

    return redirect(env.WEB_SERVER_LINK+file_id)


@app.route('/series_media/<path:id>')
def series_file(id):

    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("SELECT path FROM series WHERE id = ?", (id,))
    result = cursor.fetchone()
    conn.close()
    print(result)

    file_id = str(uuid.uuid4())
    link_path = env.WEB_SERVER_PATH + file_id
    os.symlink(result[0], link_path)

    return redirect(env.WEB_SERVER_LINK+file_id)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/movies")
def movies():
    movies = get_movies()
    return render_template("movies.html", movies=movies)


@app.route("/series")
def series():
    movies = get_series()
    return render_template("series.html", movies=movies)

if __name__ == "__main__":
    app.run(debug=True)
