import unittest

from model import Player, Movie


class TimelineTest(unittest.TestCase):
    def test_add_oldest_movie_correctly(self):
        p = Player("TestPlayer")
        mo = Movie("test", "-", "", 1800, "")
        result = p.check_correct_pos_in_timeline(mo, 0)
        self.assertTrue(result)

    def test_add_oldest_movie_incorrectly(self):
        p = Player("TestPlayer")
        mo = Movie("test", "-", "", 1800, "")
        result = p.check_correct_pos_in_timeline(mo, 1)
        self.assertFalse(result)

    def test_add_newest_movie_correctly(self):
        p = Player("TestPlayer")
        mo = Movie("test", "-", "", 2050, "")
        result = p.check_correct_pos_in_timeline(mo, 1)
        self.assertTrue(result)

    def test_add_newest_movie_incorrectly(self):
        p = Player("TestPlayer")
        mo = Movie("test", "-", "", 2050, "")
        result = p.check_correct_pos_in_timeline(mo, 0)
        self.assertFalse(result)

    def test_add_movie_with_same_year(self):
        p = Player("TestPlayer")
        mo = Movie("test", "-", "", 1800, "")
        mo2 = Movie("test3", "-", "", 1800, "")
        p.add_to_timeline(mo, 0)
        result0 = p.check_correct_pos_in_timeline(mo2, 0)
        result1 = p.check_correct_pos_in_timeline(mo2, 1)
        self.assertEqual(result0, result1)


if __name__ == '__main__':
    unittest.main()
