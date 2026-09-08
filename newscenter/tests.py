from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class DayOfWeekViewTests(TestCase):
    def test_invalid_dayofweek_returns_404(self):
        # Bots scanning for month-style archives (e.g. /news/articles/nov/)
        # were hitting this URL, which matches the dayofweek pattern with a
        # code that isn't a real day abbreviation and used to raise an
        # uncaught ValueError/KeyError (500) instead of a 404.
        response = self.client.get('/news/articles/nov/')
        self.assertEqual(response.status_code, 404)

    def test_valid_dayofweek_on_missing_newsroom_returns_404(self):
        response = self.client.get('/news/does-not-exist/mon/')
        self.assertEqual(response.status_code, 404)
