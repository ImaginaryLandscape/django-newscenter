from __future__ import absolute_import
from django.db import models

from cms.models import CMSPlugin
from newscenter.models import Feed


class NewsFeedPluginModel(CMSPlugin):
    location = models.ForeignKey(Feed)
    limit = models.IntegerField(
        'Article Limit', default=5,
        help_text="Maximum number of articles to display")

    class Meta:
        db_table = 'newscenter_newsfeedpluginmodel'

    def __str__(self):
        return self.location.name
