import unittest

from data import get_imdb_top_250_movies


class TimelineTest(unittest.TestCase):
    def test_for_250_extracted_movies(self):
        l = get_imdb_top_250_movies()
        self.assertEqual(len(l), 250)


if __name__ == '__main__':
    unittest.main()
