import csv
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup

FILE = "./data/top_250.csv"


# Reference:
# https://the-algorithms.com/es/algorithm/get-imdb-top-250-movies-csv

def get_imdb_top_250_movies() -> List[Tuple[str, int]]:
    # use this website since the original imdb top 250 has restricted access
    url = "https://250.took.nl/compare/full"
    try:
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        # extract the table containing the movies & remove the header
        table = soup.find('table', class_='list-data')
        table_rows = table.find_all('tr')
        table_rows.remove(table.find('tr', class_='tr-header'))
        titles = []
        for r in table_rows:
            # find the element containing the movie title
            title_element = r.find('span', {'title': True}).find('a')
            title = title_element.text.strip() if title_element else ""
            # find the element containing the movie year
            year_element = title_element.find_next('span', class_='hidden-links').find('a')
            year = year_element.text.strip() if year_element else 0
            titles.append((title, year))
        return titles
    except Exception:
        print(Exception)


def write_top250_to_csv():
    movies = get_imdb_top_250_movies()
    with open(FILE, "w", newline="") as out_file:
        writer = csv.writer(out_file)
        writer.writerow(["Movie", "Year"])
        for m in movies:
            writer.writerow(m)
