import csv
import json
import os
from typing import List

import requests
import tmdbv3api

from model import Movie, MovieHandler

TOP_250_FILE = "./data/top_250.csv"
OSCARS_2024_FILE = "./data/oscars_2024.csv"


def init_tmdb_api():
    json_text = json.load(open(os.path.join("./credentials.json")))
    tmdb = tmdbv3api.TMDb()
    tmdb.api_key = json_text["api_key"]
    tmdb.language = 'de'


def import_top250_movies() -> List[Movie]:
    _movies = []
    with open(TOP_250_FILE, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            m = Movie(row['Movie'], "", "", int(row['Year']), "")
            _movies.append(m)
    return _movies


def import_oscars2024_movies() -> List[Movie]:
    _movies = []
    with open(OSCARS_2024_FILE, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            m = Movie(row['Movie'], "", "", int(row['Year']), "")
            _movies.append(m)
    return _movies


def fill_missing_info(movies: List[Movie]):
    init_tmdb_api()
    tmdb_movies = tmdbv3api.Search()
    for m in movies:
        search = tmdb_movies.movies(term=m.get_name(), year=m.get_year())
        if not search:
            print(f"No TMDB entry found for: {m}")
        tmdb_m = search[0]
        if tmdb_m.title == tmdb_m.original_title:
            m.set_german_name("-")
        else:
            m.set_german_name(tmdb_m.title)
        m.set_director(get_director(tmdb_m.id))
        m.set_img(f"https://image.tmdb.org/t/p/original/{tmdb_m.backdrop_path}")


def get_director(m_id: int) -> str:
    url = f"https://api.themoviedb.org/3/movie/{m_id}/credits?language=en-US"
    json_text = json.load(open(os.path.join("./credentials.json")))
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {json_text['req_key']}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    directors = [crew_member for crew_member in data["crew"] if crew_member["job"] == "Director"]
    all_directors = directors[0]['name']
    if len(directors) > 1:
        directors.remove(directors[0])
        for d in directors:
            all_directors = f"{all_directors} & {d['name']}"
    return all_directors


def add_movies(top250=True):
    init_tmdb_api()
    movie_handler = MovieHandler()
    movies = []
    if top250:
        movies = import_top250_movies()
    else:
        movies = import_oscars2024_movies()
    fill_missing_info(movies)
    for m in movies:
        movie_handler.add_new_movie(m)
    movie_handler.export_movies()
