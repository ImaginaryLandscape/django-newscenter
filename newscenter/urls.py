from django.views.generic.list import ListView
try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls.defaults import url
from .views import (
    NewsroomIndex, NewsroomLatest, NewsroomRandom, ArticleDetail,
    ArchiveYear, ArchiveMonth, newsroom_detail, category_detail)
from .feeds import NewsroomFeed
from . import models

# ## Object List
urlpatterns = [
    url(r'^categories/$', ListView.as_view(
        queryset=models.Category.objects.all(),
        allow_empty=True,
    )),
]

# ## Custom
urlpatterns += [
    url(r'^$', NewsroomIndex.as_view(), name="news_newsroom_index"),
    url(r'^(?P<slug>[\-\d\w]+)/$', newsroom_detail,
        name='news_newsroom_detail'),
    url(r'^categories/(?P<slug>[\-\d\w]+)/$', category_detail,
        name='news_category_detail'),
    url(r'^(?P<newsroom>[\-\d\w]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<slug>[\-\d\w]+)/$',
        ArticleDetail.as_view(), name='news_article_detail'),
    url(r'^(?P<newsroom>[\-\d\w]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
        ArchiveMonth.as_view(), name='news_archive_month',),
    url(r'^(?P<newsroom>[\-\d\w]+)/(?P<year>\d{4})/$',
        ArchiveYear.as_view(), name='news_archive_year',),
    url(r'^(?P<newsroom>[\-\d\w]+)/latest/$',
        NewsroomLatest.as_view(), name='news_newsroom_latest'),
    url(r'^(?P<newsroom>[\-\d\w]+)/random/$',
        NewsroomRandom.as_view(), name='news_newsroom_random')
]

# ## Feeds
urlpatterns += [
    url(r'^(?P<newsroom>[\-\d\w]+)/rss/$', NewsroomFeed(), {}, name='newsroom_feed'),
]
