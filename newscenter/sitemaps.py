from django.contrib.sitemaps import Sitemap
from newscenter.models import Newsroom, Article


class NewsroomSitemap(Sitemap):
    def items(self):
        return Newsroom.objects.all()

    def lastmod(self, obj):
        return obj.modified


class ArticleSiteMap(Sitemap):
    def items(self):
        return Article.objects.get_published()

    def lastmod(self, obj):
        return obj.modified

