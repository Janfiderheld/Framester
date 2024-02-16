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
        p = Player("TestPlayer", False)
        mo = Movie("test", "-", "", 1800, "")
        mo2 = Movie("test2", "-", "", 1800, "")
        p.add_to_timeline(mo, 0)
        result0 = p.check_correct_pos_in_timeline(mo2, 0)
        result1 = p.check_correct_pos_in_timeline(mo2, 1)
        self.assertEqual(result0, result1)

    def test_add_multiple_movie_with_same_year(self):
        p = Player("TestPlayer", False)
        mo = Movie("test1", "-", "", 2023, "")
        mo2 = Movie("test2", "-", "", 2023, "")
        mo3 = Movie("test3", "-", "", 2023, "")
        p.add_to_timeline(mo, 0)
        p.add_to_timeline(mo2, 0)
        result0 = p.check_correct_pos_in_timeline(mo3, 0)
        result1 = p.check_correct_pos_in_timeline(mo3, 1)
        result2 = p.check_correct_pos_in_timeline(mo3, 2)
        self.assertTrue(result0)
        self.assertTrue(result1)
        self.assertTrue(result2)

    def test_add_movie_with_same_year_at_end(self):
        p = Player("TestPlayer", False)
        for i in range(0, p.max_points-1):
            m = Movie(f"test{i}", "-", "", 2023, "")
            p.add_to_timeline(m, i)
        last_m = Movie("last_test", "-", "", 2023, "")
        result = p.check_correct_pos_in_timeline(last_m, p.max_points-1)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
