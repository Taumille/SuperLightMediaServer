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
        self.episode = "S00E00"


def extract_base_name(path, basepath_variable):
    # Normalize the path and split into components
    path_components = os.path.normpath(path).split(os.sep)

    # Split the basepath_variable into components
    basepath_components = os.path.normpath(basepath_variable).split(os.sep)

    # The number of components in the basepath_variable
    basepath_length = len(basepath_components)

    # Extract the components up to "Name" (basepath_length + 1)
    base_name_components = path_components[:basepath_length + 1]

    # Reconstruct the path
    base_name = os.sep.join(base_name_components)
    return base_name


class MovieDB:
    def __init__(self):
        self.con = sqlite3.connect("movies.db")
        self.cur = self.con.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS movies(id INTEGER PRIMARY KEY AUTOINCREMENT, name, description, year, path, tmdbid)")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS series(id INTEGER PRIMARY KEY AUTOINCREMENT, series_name, description, year, path, episode, tmdbid)")
        self.con.commit()
        self.tmdb = tmdbv3api.TMDb()
        self.tmdb.api_key = env.SECRET_API_KEY
        self.tmdb.language = env.TMDB_LANGUAGE
        self.movie_tmbd = tmdbv3api.Movie()
        self.tv_tmbd = tmdbv3api.TV()

    def create_new_entry_movie(self, movie: Movie):
        self.cur.execute("SELECT 1 FROM movies WHERE description = ?", (movie.desc,))
        res = self.cur.fetchone()
        if res:
            return res[0]
        self.cur.execute(
            "INSERT OR IGNORE INTO movies (name, description, year, path, tmdbid) VALUES (?,?,?,?,?)",
            (movie.name, movie.desc, movie.date, movie.path, movie.tmdbid))
        self.con.commit()
        return self.cur.lastrowid

    def create_new_entry_series(self, movie: Movie):
        self.cur.execute(
            "INSERT OR IGNORE INTO series (series_name, description, year, path, episode, tmdbid) VALUES (?,?,?,?,?,?)",
            (movie.name, movie.desc, movie.date, movie.path, movie.episode, movie.tmdbid))
        self.con.commit()
        return self.cur.lastrowid

    def tmdb_search_series(self, cleaner: Cleaner):
        tv = Movie()
        tv.episode = cleaner.episode
        self.cur.execute("SELECT * FROM series WHERE path LIKE ? LIMIT 1",
                         (f"%{extract_base_name(cleaner.path,
                                                env.SERIES_PATH)}%",))
        result = self.cur.fetchone()
        print(f"Series : {cleaner.path} result : {result}")
        if result is not None:
            tv.name = result[1]
            tv.desc = result[2]
            tv.date = result[3]
            tv.path = cleaner.path
            tv.tmdbid = result[6]
            id = self.create_new_entry_series(tv)
            return
        search = self.tv_tmbd.search(cleaner.filename)
        if (search.total_results == 0):
            tv.name = cleaner.filename
            tv.desc = "Unknown"
            tv.date = 1900
            tv.path = cleaner.path
            tv.tmdbid = 0
            id = self.create_new_entry_series(tv)
            shutil.copy("static/pictures/none.jpg",
                        "static/pictures/"+str(tv.name)+".jpg")
            return tv

        good_res = search[0]
        tv.name = good_res.name
        tv.desc = good_res.overview
        tv.date = good_res.first_air_date
        tv.path = cleaner.path
        tv.tmdbid = good_res.id
        self.create_new_entry_series(tv)
        self.download_picture(good_res.poster_path, good_res.name)

    def tmdb_search_movie(self, cleaner: Cleaner):
        search = self.movie_tmbd.search(cleaner.filename)
        movie = Movie()
        movie.date = cleaner.date
        if (search.total_results == 0):
            movie.name = cleaner.filename
            movie.desc = "Unknown"
            movie.date = 1900
            movie.path = cleaner.path
            movie.tmdbid = 0
            id = self.create_new_entry_movie(movie)
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
        id = self.create_new_entry_movie(movie)
        self.download_picture(good_res.poster_path, id)

    def download_picture(self, filename: str, id):
        if filename is None:
            shutil.copy("static/pictures/none.jpg",
                        "static/pictures/"+str(id)+".jpg")
            return

        url = "https://image.tmdb.org/t/p/w1280"+ filename
        filename = wget.download(url)

        os.rename(filename, "static/pictures/"+str(id)+".jpg")
