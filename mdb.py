import sqlite3
import tmdbv3api
import env
import os
import shutil
from cleaner import Cleaner
import wget

class Movie:
    def __init__(self):
        self.name = ""
        self.path = ""
        self.date = 1900
        self.desc = ""
        self.tmdbid = 0

class MovieDB:
    def __init__(self):
        self.con = sqlite3.connect("movies.db")
        self.cur = self.con.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS movies(id INTEGER PRIMARY KEY AUTOINCREMENT, name, description, year, path, tmdbid)")
        self.con.commit()
        self.tmdb = tmdbv3api.TMDb()
        self.tmdb.api_key = env.SECRET_API_KEY
        self.tmdb.language = env.TMDB_LANGUAGE
        self.movie_tmbd = tmdbv3api.Movie()

    def create_new_entry(self, movie: Movie):
        self.cur.execute("SELECT 1 FROM movies WHERE description = ?", (movie.desc,))
        res = self.cur.fetchone()
        if res:
            return res[0]
        self.cur.execute(
            "INSERT OR IGNORE INTO movies (name, description, year, path, tmdbid) VALUES (?,?,?,?,?)",
            (movie.name, movie.desc, movie.date, movie.path, movie.tmdbid))
        self.con.commit()
        return self.cur.lastrowid

    def tmdb_search(self, cleaner: Cleaner):
        search = self.movie_tmbd.search(cleaner.filename)
        movie = Movie()
        movie.date = cleaner.date
        if (search.total_results == 0):
            movie.name = cleaner.filename
            movie.desc = "Unknown"
            movie.date = 1900
            movie.path = cleaner.path
            movie.tmdbid = 0
            id = self.create_new_entry(movie)
            shutil.copy("static/pictures/none.jpg",
                        "static/pictures/"+str(id)+".jpg")
            return movie


        if (cleaner.date == 1900):
            print("Clearly no date")
            good_res = search[0]
        else:
            # Find the nearest movie
            smallest_gap = 100
            for res in search:
                try:
                    year = int(res.release_date[:4])
                    if abs(year - movie.date) < smallest_gap:
                        smallest_gap = abs(year - movie.date)
                        print(f"{year} - {movie.date}")
                        good_res = res
                except:
                    pass

        print(good_res)
        movie.name = good_res.title
        movie.desc = good_res.overview
        movie.date = good_res.release_date
        movie.path = cleaner.path
        movie.tmdbid = good_res.id
        id = self.create_new_entry(movie)
        self.download_picture(good_res.poster_path, id)

    def download_picture(self, filename: str, id):
        url = "https://image.tmdb.org/t/p/w1280"+ filename
        filename = wget.download(url)

        os.rename(filename, "static/pictures/"+str(id)+".jpg")
