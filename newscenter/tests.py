from datetime import timedelta

from django.test import TestCase, override_settings
from django.utils import timezone

from newscenter import models


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


class NewsroomRedirectViewTests(TestCase):
    # The latest/random/random_featured views redirect to an article picked
    # from a queryset. When that queryset is empty (a new newsroom, every
    # article expired, or nothing featured) they used to raise an uncaught
    # IndexError (500) instead of a 404.
    def setUp(self):
        self.newsroom = models.Newsroom.objects.create(
            name='Press', slug='press')
        self.empty_newsroom = models.Newsroom.objects.create(
            name='Empty', slug='empty')
        self.category = models.Category.objects.create(
            title='Events', slug='events')

    def create_article(self, **kwargs):
        defaults = {
            'title': 'Hello',
            'newsroom': self.newsroom,
            'release_date': timezone.now() - timedelta(days=1),
        }
        defaults.update(kwargs)
        return models.Article.objects.create(**defaults)

    def test_latest_on_empty_newsroom_returns_404(self):
        response = self.client.get('/news/empty/latest/')
        self.assertEqual(response.status_code, 404)

    def test_latest_ignores_unpublished_articles(self):
        self.create_article(newsroom=self.empty_newsroom, active=False)
        response = self.client.get('/news/empty/latest/')
        self.assertEqual(response.status_code, 404)

    def test_latest_on_missing_newsroom_returns_404(self):
        response = self.client.get('/news/does-not-exist/latest/')
        self.assertEqual(response.status_code, 404)

    def test_latest_redirects_to_newest_article(self):
        self.create_article(title='Older',
            release_date=timezone.now() - timedelta(days=3))
        newest = self.create_article(title='Newest')
        response = self.client.get('/news/press/latest/')
        self.assertRedirects(response, newest.get_absolute_url(),
            fetch_redirect_response=False)

    def test_random_on_empty_newsroom_returns_404(self):
        response = self.client.get('/news/empty/random/')
        self.assertEqual(response.status_code, 404)

    def test_random_with_unmatched_category_returns_404(self):
        self.create_article()
        response = self.client.get('/news/press/random/?category=events')
        self.assertEqual(response.status_code, 404)

    def test_random_redirects_to_article(self):
        article = self.create_article()
        response = self.client.get('/news/press/random/')
        self.assertRedirects(response, article.get_absolute_url(),
            fetch_redirect_response=False)

    def test_random_with_category_redirects_to_article(self):
        self.create_article(title='Other')
        article = self.create_article(title='Tagged')
        article.categories.add(self.category)
        response = self.client.get('/news/press/random/?category=events')
        self.assertRedirects(response, article.get_absolute_url(),
            fetch_redirect_response=False)

    @override_settings(NEWSCENTER_INCLUDE_RANDOM_FEATURED_NEWSROOMS=['press'])
    def test_random_featured_without_featured_articles_returns_404(self):
        self.create_article(featured=False)
        response = self.client.get('/news/random_featured/')
        self.assertEqual(response.status_code, 404)

    def test_random_featured_without_setting_returns_404(self):
        self.create_article(featured=True)
        response = self.client.get('/news/random_featured/')
        self.assertEqual(response.status_code, 404)

    @override_settings(NEWSCENTER_INCLUDE_RANDOM_FEATURED_NEWSROOMS=['press'])
    def test_random_featured_redirects_to_featured_article(self):
        article = self.create_article(featured=True)
        response = self.client.get('/news/random_featured/')
        self.assertRedirects(response, article.get_absolute_url(),
            fetch_redirect_response=False)
