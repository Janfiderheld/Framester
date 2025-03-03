import matplotlib.pyplot as plt

from model import MovieHandler

mh = MovieHandler()


def visualise_year_dist():
    years = {y: 0 for y in range(1920, 2026)}
    for mov in mh.copy_all_movies():
        years[mov.get_year()] += 1

    x = list(years.keys())
    y = list(years.values())
    plt.figure(figsize=(16, 6))
    plt.bar(x, y, color='skyblue', edgecolor='black')
    for i, v in enumerate(y):
        if v > 0:
            plt.text(x[i], v + 0.5, str(v), ha='center', fontsize=10)

    plt.xlabel("Years")
    plt.ylabel("Amount")
    plt.xticks(rotation=45)
    plt.yticks(range(0, 20, 1))
    plt.ylim(0, 20)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig("./year_distribution.png")
    plt.show()


if __name__ == "__main__":
    visualise_year_dist()
