from typing import List

from model import Movie


class Player:
    MAX_TOKENS = 2
    POINTS_TO_WIN = 8

    def __init__(self, name: str):
        self.__name = name
        self.__tokens = Player.MAX_TOKENS
        self.__timeline: List[Movie] = []
        self.get_starting_movie()

    def get_name(self) -> str:
        return self.__name

    def get_current_token(self) -> int:
        return self.__tokens

    def get_timeline(self) -> List[Movie]:
        return self.__timeline

    def check_win(self) -> bool:
        return len(self.__timeline) >= self.POINTS_TO_WIN

    def reset(self):
        self.__tokens = Player.MAX_TOKENS
        self.get_starting_movie()

    def get_starting_movie(self):
        from model import MovieHandler
        mh = MovieHandler()
        self.__timeline.clear()
        self.__timeline.append(mh.return_rand_movie())

    def check_correct_pos_in_timeline(self, m: Movie, pos: int) -> bool:
        assert pos <= len(self.__timeline)

        corr_p = 0
        two_slots = False
        for t in self.__timeline:
            if t.get_year() < m.get_year():
                corr_p += 1
            elif t.get_year() == m.get_year():
                two_slots = True
                break
            else:
                break
        if two_slots:
            return pos == corr_p or pos == corr_p+1
        else:
            return pos == corr_p

    def add_to_timeline(self, m: Movie, pos: int):
        assert pos <= len(self.__timeline)
        assert self.check_correct_pos_in_timeline(m, pos)

        self.__timeline.insert(pos, m)

    def __str__(self) -> str:
        return f"{self.__name} ({self.__tokens}/{Player.MAX_TOKENS} Tokens) - Timeline: {len(self.__timeline)}/{self.POINTS_TO_WIN}"
