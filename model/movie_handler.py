import csv
import random
from typing import List
from model import Movie, SingletonMeta


# Singleton
class MovieHandler(metaclass=SingletonMeta):
    DATA_FILE = "./data/movies.csv"

    def __init__(self):
        self.__movies = self.import_movies()
        self.__current_movies = self.__movies.copy()

    @staticmethod
    def import_movies() -> List[Movie]:
        _movies = []
        try:
            with open(MovieHandler.DATA_FILE, mode='r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    m = Movie(row['Name'], row['Name (German)'], row['Director'], int(row['Year']), row['Image URL'])
                    _movies.append(m)
        except Exception:
            _movies.append(Movie("Test", "-", "Test", 2000, ""))

        print(f"Imported {len(_movies)} movies from {MovieHandler.DATA_FILE}")
        return _movies

    def export_movies(self):
        with open(MovieHandler.DATA_FILE, mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['Name', 'Name (German)', 'Director', 'Year', 'Image URL']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for m in self.__movies:
                writer.writerow({
                    'Name': m.get_name(),
                    'Name(German)': m.get_german_name(),
                    'Director': m.get_director(),
                    'Year': m.get_year(),
                    'Image URL': m.get_img()
                })

    def check_movie_existence(self, new_m: Movie) -> bool:
        for m in self.__movies:
            if m == new_m:
                return True
        return False

    def add_new_movie(self, new_m: Movie):
        if self.check_movie_existence(new_m):
            print(f"Movie {new_m} already exists")
            return

        self.__movies.append(new_m)
        print(f"Movie {str(new_m)} is added with img: {new_m.get_img()}")

    def return_rand_movie(self) -> Movie:
        if len(self.__current_movies) == 0:
            self.reset_current_movie_list()
        m = random.choice(self.__current_movies)
        self.__current_movies.remove(m)
        return m

    def reset_current_movie_list(self):
        self.__current_movies = self.__movies.copy()
