class Movie:
    def __init__(self, name: str, ger_name: str, direct: str, year: int, img_file: str):
        self.__name = name
        self.__german_name = ger_name
        self.__director = direct
        self.__year = year
        self.__image = img_file

    def get_name(self) -> str:
        return self.__name

    def get_german_name(self) -> str:
        return self.__german_name

    def get_director(self) -> str:
        return self.__director

    def get_year(self) -> int:
        return self.__year

    def get_img(self) -> str:
        return self.__image

    def __eq__(self, other) -> bool:
        """Overrides the default implementation"""
        if isinstance(other, Movie):
            return (self.__name == other.__name) & (self.__director == other.__director) & (self.__year == other.__year)
        return False

    def __str__(self) -> str:
        title = self.__name
        if self.__name != self.__german_name and self.__german_name != '-':
            title += f" (dt. {self.__german_name})"
        return f"{title} ({self.__year}) by {self.__director}"
