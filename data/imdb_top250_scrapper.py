import csv

import requests
from bs4 import BeautifulSoup

FILE = "./data/top_250.csv"


# Reference:
# https://the-algorithms.com/es/algorithm/get-imdb-top-250-movies-csv

def get_imdb_top_250_movies() -> [(str, int)]:
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
            titles.append((title, int(year)))
        return titles
    except Exception:
        print(Exception)


def read_existing_top250() -> [(str, int)]:
    result = []
    with open(FILE, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            movie_name = row[0]
            year = int(row[1])
            result.append((movie_name, year))
    return result


def remove_existing(movies: [(str, int)]):
    top250 = read_existing_top250()
    new = []
    for m in movies:
        exists = False
        for tm in top250:
            if m[0] == tm[0] and m[1] == tm[1]:
                exists = True
                continue
        if not exists:
            new.append(m)
    return new


def write_top250_to_csv(update: bool):
    current_top250 = get_imdb_top_250_movies()
    if update:
        movies = remove_existing(current_top250)
        with open(FILE, mode='a+', newline='', encoding='utf-8') as out_file:
            writer = csv.writer(out_file)
            for m in movies:
                writer.writerow(m)
    else:
        movies = current_top250
        with open(FILE, mode='w', newline='', encoding='utf-8') as out_file:
            writer = csv.writer(out_file)
            writer.writerow(["Movie", "Year"])
            for m in movies:
                writer.writerow(m)
