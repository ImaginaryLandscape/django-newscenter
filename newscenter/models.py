from datetime import datetime
from django.db import models
from django.contrib.syndication.views import Feed
from random import choice
from newscenter import managers
import PIL
from django.conf import settings

class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(
        help_text='Automatically generated from the title.'
    )
    
    class Meta:
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('news_category_detail', [str(self.slug)])

    def get_article_count(self):
        return Category.objects.filter(slug=self.slug).annotate(
            article_count=models.Count('articles'))[0].article_count

class Newsroom(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    
    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' %(self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('news_newsroom_detail', [str(self.slug)])


class Location(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    
    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' %(self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('news_location_detail', [str(self.slug)])


class Article(models.Model):
    title = models.CharField(max_length=400)
    location = models.ForeignKey(Location, blank=True, null=True)
    slug = models.SlugField('ID', unique=True,
        unique_for_date='release_date',
        help_text='Automatically generated from the title.'
    )
    body = models.TextField()
    teaser = models.TextField(blank=True, 
        help_text="A summary preview of the article.")
    release_date = models.DateTimeField('Publication Date', 
        default=datetime.now)
    expire_date = models.DateTimeField('Expiration Date', null=True, blank=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    categories = models.ManyToManyField('Category', related_name='articles', 
        null=True, blank=True)    
    newsroom = models.ForeignKey(Newsroom, null=True, blank=True, 
        related_name='articles',default=1)
    objects = managers.ArticleManager()

    class Meta:
        ordering = ('-release_date',)
        get_latest_by = 'release_date'

    def random_thumbnail(self):
        if self.images.filter(thumbnail=True).count() > 0:
            return choice(self.images.filter(thumbnail=True))

    def __unicode__(self):
        return u'%s' %(self.title)

    def get_absolute_url(self):
        return ('news_article_detail', (), { 
             'newsroom': self.newsroom.slug,
             'year': self.release_date.strftime('%Y'),
             'month': self.release_date.strftime('%b').lower(),
             'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)

    def get_previous_published(self):
        try: 
            return self.get_previous_by_release_date(active=True, 
            newsroom=self.newsroom, expire_date__gte=datetime.now, 
            release_date__lte=datetime.now())
        except:
            return self.get_previous_by_release_date(active=True, 
            newsroom=self.newsroom, expire_date__isnull=True, 
            release_date__lte=datetime.now())
     
    def get_next_published(self):
        try:
            return self.get_next_by_release_date(active=True, 
            newsroom=self.newsroom, expire_date__gte=datetime.now, 
            release_date__lte=datetime.now())
        except:
            return self.get_next_by_release_date(active=True, 
            newsroom=self.newsroom, expire_date__isnull=True, 
            release_date__lte=datetime.now())


class Image(models.Model):
    image = models.ImageField(blank=False, upload_to='newscenter_uploads',
        help_text="Images larger than 800x600 will be resized")
    article = models.ForeignKey(Article, related_name='images')
    caption = models.CharField(max_length=200, blank=True)
    name = models.CharField('description', max_length=100, blank=True, 
        help_text="This will be used for alt text.")
    thumbnail = models.BooleanField('Use as Thumbnail', default=False, 
        help_text="To be displayed on article listing pages. If more than "
                  "one is selected, the thumbnail used will be chosen at "
                  "random.")
    sort = models.IntegerField(default=0)

    class Meta:
        ordering = ('sort',)

    def save(self):
        super(Image, self).save()
        if self.image:
            filename = self.image.path
            image = PIL.Image.open(filename)
            try:
                width = settings.NEWSCENTER_IMAGE_WIDTH
            except:
                width = 800
            try:
                height = settings.NEWSCENTER_IMAGE_HEIGHT
            except:
                height = 600
            try:
                imquality = settings.NEWSCENTER_IMAGE_QUALITY
            except:
                imquality = 100
            size=(width, height)
            image.thumbnail(size, PIL.Image.ANTIALIAS)
            image.save(filename, quality=imquality)

