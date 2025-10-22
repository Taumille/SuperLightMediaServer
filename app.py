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

@app.route("/")
def index():
    movies = get_movies()
    return render_template("index.html", movies=movies)

if __name__ == "__main__":
    app.run(debug=True)
