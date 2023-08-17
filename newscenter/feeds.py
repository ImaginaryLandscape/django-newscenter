from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from newscenter.models import Article, Newsroom


class NewsroomFeed(Feed):
    def get_object(self, request, newsroom, website=None):
        try:
            return get_object_or_404(Newsroom, slug=newsroom, website__short_name=website)
        except:
            return get_object_or_404(Newsroom, slug=newsroom)

    def title(self, obj):
        return "%s Entries" % obj.name

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return "Latest entries posted in %s" % obj.name

    def items(self, obj):
        return Article.objects.get_published().filter(newsroom=obj)

    def item_pubdate(self, item):
        return item.release_date
