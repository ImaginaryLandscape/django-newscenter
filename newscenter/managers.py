from datetime import datetime
from django.db import models


class ArticleManager(models.Manager):

    def get_published(self):
        return self.filter(
            models.Q(expire_date__gte=datetime.now()) |
            models.Q(expire_date__isnull=True)).filter(
            active=True, release_date__lte=datetime.now())

    def get_featured(self):
        return self.filter(
            models.Q(expire_date__gte=datetime.now()) |
            models.Q(expire_date__isnull=True)).filter(
            active=True, release_date__lte=datetime.now(), featured=True)
