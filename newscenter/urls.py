from datetime import datetime
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.dates import YearArchiveView, MonthArchiveView
try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url
from newscenter.views import ArchiveYear, ArchiveMonth
from newscenter.feeds import NewsroomFeed
from newscenter import models 

##Object List
urlpatterns = patterns('',
    url(r'^$', ListView.as_view(
        queryset=models.Newsroom.objects.all(), 
        allow_empty=True,
    ), name='newscenter_index'),
    url(r'^categories/$', ListView.as_view(
        queryset=models.Newsroom.objects.all(), 
        allow_empty=True,
    )),
)

##Custom 
urlpatterns += patterns('newscenter.views',
    url(r'^(?P<slug>[\-\d\w]+)/$',
        'newsroom_detail', name='news_newsroom_detail'),
    url(r'^categories/(?P<slug>[\-\d\w]+)/$',
        'category_detail', name='news_category_detail'),
    url(r'^(?P<newsroom>[\-\d\w]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<slug>[\-\d\w]+)/$',
        'article_detail', name='news_article_detail'),
    url(r'^(?P<newsroom>[\-\d\w]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
        ArchiveMonth.as_view(), name='news_archive_month',),
    url(r'^(?P<newsroom>[\-\d\w]+)/(?P<year>\d{4})/$', 
        ArchiveYear.as_view(), name='news_archive_year',)
)

##Feeds
urlpatterns += patterns('',
    (r'^(?P<newsroom>[\-\d\w]+)/rss/$', NewsroomFeed(), None, 'newsroom_feed'),
)
