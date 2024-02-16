import sys
from typing import List

from model import Movie


class Player:
    max_points = 8

    def __init__(self, name: str, add_start_movie=True):
        self.__name = name
        self.__timeline: List[Movie] = []
        if add_start_movie:
            self.get_starting_movie()

    def get_name(self) -> str:
        return self.__name

    def get_timeline(self) -> List[Movie]:
        return self.__timeline

    def check_win(self) -> bool:
        return len(self.__timeline) >= self.max_points

    def reset(self):
        self.get_starting_movie()

    def get_starting_movie(self):
        from model import MovieHandler
        mh = MovieHandler()
        self.__timeline.clear()
        self.__timeline.append(mh.return_rand_movie())

    def check_correct_pos_in_timeline(self, m: Movie, pos: int) -> bool:
        assert pos <= len(self.__timeline)

        if len(self.__timeline) == 0:
            return True

        first = sys.maxsize
        last = -1
        for t in self.__timeline:
            idx = self.__timeline.index(t)
            # Case 1: t is older
            if t.get_year() < m.get_year():
                first = idx + 1
                last = idx + 1
                continue
            # Case 2: both movies are from the same year
            if t.get_year() == m.get_year():
                first = min(idx, first)
                last = max(idx+1, last)
                continue
            # Case 3: new movie is older
            if m.get_year() < t.get_year():
                first = idx
                last = idx
        return first <= pos <= last

    def add_to_timeline(self, m: Movie, pos: int):
        assert pos <= len(self.__timeline)
        assert self.check_correct_pos_in_timeline(m, pos)

        self.__timeline.insert(pos, m)

    def __str__(self) -> str:
        return f"{self.__name} - Timeline: {len(self.__timeline)}/{self.max_points}"
