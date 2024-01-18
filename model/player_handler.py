from typing import List

from model import Player, SingletonMeta


# Singleton
class PlayerHandler(metaclass=SingletonMeta):
    def __init__(self):
        self.__players: List[Player] = []
        self.__player_idx = 0

    def add_new_player(self, p: Player):
        self.__players.append(p)

    def return_current_player(self) -> Player:
        return self.__players[self.__player_idx]

    def goto_next_player(self):
        if self.__player_idx == (len(self.__players)-1):
            self.__player_idx = 0
        else:
            self.__player_idx += 1
