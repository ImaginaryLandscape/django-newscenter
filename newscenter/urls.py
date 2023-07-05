from django.views.generic.list import ListView
try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import include
from .views import (
    NewsroomIndex, NewsroomLatest, NewsroomRandom, ArticleDetail,
    ArchiveYear, ArchiveMonth, newsroom_detail, category_detail)
from .feeds import NewsroomFeed
from . import models

# ## Object List
urlpatterns = [
    re_path(r'^categories/$', ListView.as_view(
        queryset=models.Category.objects.all(),
        allow_empty=True,
    )),
]

# ## Custom
urlpatterns += [
    re_path(r'^$', NewsroomIndex.as_view(), name="news_newsroom_index"),
    re_path(r'^(?P<slug>[\-\d\w]+)/$', newsroom_detail,
        name='news_newsroom_detail'),
    re_path(r'^categories/(?P<slug>[\-\d\w]+)/$', category_detail,
        name='news_category_detail'),
    re_path(r'^(?P<newsroom>[\-\d\w]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<slug>[\-\d\w]+)/$',
        ArticleDetail.as_view(), name='news_article_detail'),
    re_path(r'^(?P<newsroom>[\-\d\w]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
        ArchiveMonth.as_view(), name='news_archive_month',),
    re_path(r'^(?P<newsroom>[\-\d\w]+)/(?P<year>\d{4})/$',
        ArchiveYear.as_view(), name='news_archive_year',),
    re_path(r'^(?P<newsroom>[\-\d\w]+)/latest/$',
        NewsroomLatest.as_view(), name='news_newsroom_latest'),
    re_path(r'^(?P<newsroom>[\-\d\w]+)/random/$',
        NewsroomRandom.as_view(), name='news_newsroom_random')
]

# ## Feeds
urlpatterns += [
    re_path(r'^(?P<newsroom>[\-\d\w]+)/rss/$', NewsroomFeed(), {}, name='newsroom_feed'),
]
