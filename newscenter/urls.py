from datetime import datetime
from django.conf.urls.defaults import *
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.dates import YearArchiveView, MonthArchiveView
from newscenter.feeds import NewsroomFeed

from newscenter import models 

##Object List
urlpatterns = patterns('',
    (r'^$', ListView.as_view(
        queryset=models.Newsroom.objects.all(), 
        allow_empty=True,
    ), 'newscenter_index'),
    (r'^categories/$', ListView.as_view(
        queryset=models.Newsroom.objects.all(), 
        allow_empty=True,
    )),
)

##Custom 
urlpatterns += patterns('newscenter.views',
    (r'^(?P<slug>[\-\d\w]+)/$',
        'newsroom_detail', None, 'news_newsroom_detail'),
    (r'^categories/(?P<slug>[\-\d\w]+)/$',
        'category_detail', None, 'news_category_detail'),
    (r'^(?P<newsroom>[\-\d\w]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<slug>[\-\d\w]+)/$',
        'article_detail', None, 'news_article_detail'),
    (r'^(?P<newsroom>[\-\d\w]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
        MonthArchiveView.as_view(), None, 'news_archive_month',),
    (r'^(?P<newsroom>[\-\d\w]+)/(?P<year>\d{4})/$', 
        YearArchiveView.as_view(), None, 'news_archive_year',)
)

##Feeds
urlpatterns += patterns('',
    (r'^(?P<newsroom>[\-\d\w]+)/rss/$', NewsroomFeed(), None, 'newsroom_feed'),
)
