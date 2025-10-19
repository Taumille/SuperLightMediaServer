import os
from cleaner import Cleaner
from mdb import MovieDB
import tmdbv3api

def browse_subdir(path: str, extensions: tuple = ('.mkv', '.avi', '.mp4', '.mov', '.flv', '.wmv')):
    video_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.lower().endswith(extensions):
                video_files.append(os.path.join(root, file))
    return video_files

if __name__ == "__main__":
    movie_list = browse_subdir("/data/Movies/Movies")
    c = Cleaner()
    for movie in movie_list:
        print("\n")
        print(c.full_clean(movie))
        db = MovieDB()
        db.tmdb_search(c)
