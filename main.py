import os
import env
import time
from cleaner import Cleaner
from mdb import MovieDB
import sqlite3


def browse_subdir(path: str, extensions: tuple = ('.mkv', '.avi', '.mp4', '.mov', '.flv', '.wmv')):
    video_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.lower().endswith(extensions) or extensions == ("all"):
                video_files.append(os.path.join(root, file))
    return video_files


def worker_removelink():
    # For each link, get its creation date and remove link from more than a
    # day
    file_list = browse_subdir(env.WEB_SERVER_PATH,
                              ("all"))
    for file in file_list:
        if (abs(os.lstat(file).st_ctime - time.time())) > 86400:
            print(f"Removing {file}")
            os.remove(file)


def worker_addentries_movie(c, db):
    file_list = browse_subdir(env.MOVIE_PATH)
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    for file in file_list:
        cur.execute("SELECT 1 FROM movies WHERE path = ?", (file,))
        result = cur.fetchone()
        if result is None:
            print(c.full_clean_movie(file))
            db.tmdb_search_movie(c)


def worker_addentries_series(c, db):
    file_list = browse_subdir(env.SERIES_PATH)
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    for file in file_list:
        cur.execute("SELECT 1 FROM series WHERE path = ?", (file,))
        result = cur.fetchone()
        if result is None:
            print(c.full_clean_series(file))
            db.tmdb_search_series(c)


def scheduler(c, db):
    while True:
        worker_removelink()
        worker_addentries_series(c, db)
        worker_addentries_movie(c, db)
        print("done")
        time.sleep(10)


if __name__ == "__main__":
    c = Cleaner()
    db = MovieDB()
    scheduler(c, db)
