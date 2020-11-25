from datetime import datetime
from django.db import models
from django.urls import reverse
from random import choice
from newscenter import managers
import PIL
from django.conf import settings
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(
        help_text='Automatically generated from the title.'
    )

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_category_detail', args=[str(self.slug)])

    def get_article_count(self):
        return Category.objects.filter(slug=self.slug).annotate(
            article_count=models.Count('articles'))[0].article_count


class Contact(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return u'%s' % (self.name)


class Newsroom(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    if 'site_config.backends.model_backend' in settings.INSTALLED_APPS:
        website = models.ForeignKey('site_config.Website', null=True, 
            blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        if hasattr(self, 'website') and self.website:
            return u'%s | %s' % (self.name, self.website.name)
        else:
            return u'%s' % (self.name)

    def get_absolute_url(self):
        if hasattr(self, 'website') and self.website:
            return reverse(
                'news_newsroom_detail', args=[
                    str(self.website.short_name), str(self.slug)])
        else:
            return reverse('news_newsroom_detail', args=[str(self.slug)])


class Feed(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return u'%s' % (self.name)


class Location(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return u'%s' % (self.name)

    def get_absolute_url(self):
        return reverse('news_location_detail', args=[str(self.slug)])


class Article(models.Model):
    title = models.CharField(max_length=400)
    location = models.ForeignKey(Location, blank=True, null=True,
        help_text="Primary location, appearing on the article detail page",
        on_delete=models.SET_NULL)
    feeds = models.ManyToManyField(
        Feed, blank=True,
        related_name='articles', help_text="Select all areas in which this "
        "article should be listed")
    contacts = models.ManyToManyField(Contact, blank=True)
    slug = models.SlugField(
        'ID', unique=True, blank=True,
        unique_for_date='release_date',
        help_text='Automatically generated from the title.'
    )
    body = models.TextField(blank=True)
    teaser = models.TextField(
        blank=True, help_text="A summary preview of the article.")
    release_date = models.DateTimeField(
        'Publication Date', default=datetime.now)
    expire_date = models.DateTimeField('Expiration Date', null=True, blank=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    categories = models.ManyToManyField(
        'Category', related_name='articles', blank=True)
    newsroom = models.ForeignKey(Newsroom, related_name='articles', default=1,
        on_delete=models.CASCADE)
    objects = managers.ArticleManager()

    class Meta:
        ordering = ('-release_date',)
        get_latest_by = 'release_date'
        permissions = (
            ("can_feature", "Can feature an article"),
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def random_thumbnail(self):
        if self.images.filter(thumbnail=True).count() > 0:
            return choice(self.images.filter(thumbnail=True))

    def __str__(self):
        return u'%s' % (self.title)

    def get_absolute_url(self):

        url_kwargs = {
           'newsroom': self.newsroom.slug,
           'year': self.release_date.strftime('%Y'),
           'month': self.release_date.strftime('%b').lower(),
           'slug': self.slug
        }

        if hasattr(self.newsroom, 'website') and self.newsroom.website:
            url_kwargs.update({
                'website': self.newsroom.website.short_name,
            })

        return reverse('news_article_detail', kwargs=url_kwargs)

    def get_previous_published(self):
        try:
            return self.get_previous_by_release_date(
                active=True,
                newsroom=self.newsroom, expire_date__gte=datetime.now,
                release_date__lte=datetime.now())
        except:
            return self.get_previous_by_release_date(
                active=True,
                newsroom=self.newsroom, expire_date__isnull=True,
                release_date__lte=datetime.now())

    def get_next_published(self):
        try:
            return self.get_next_by_release_date(
                active=True,
                newsroom=self.newsroom, expire_date__gte=datetime.now,
                release_date__lte=datetime.now())
        except:
            return self.get_next_by_release_date(
                active=True,
                newsroom=self.newsroom, expire_date__isnull=True,
                release_date__lte=datetime.now())


class Image(models.Model):
    image = models.ImageField(
        blank=False, upload_to='newscenter_uploads',
        help_text="Images larger than the configured dimensions will be resized")
    article = models.ForeignKey(Article, related_name='images', 
        on_delete=models.CASCADE)
    name = models.CharField('description', max_length=255,
        help_text="This will be used for the image alt text.")
    caption = models.CharField(max_length=255, blank=True, help_text="Text "
        "to be displayed below the image.")
    thumbnail = models.BooleanField(
        'Use as Thumbnail', default=False,
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
                from newscenter import NewscenterSiteConfig
                config = NewscenterSiteConfig(
                    website=self.article.newsroom.website.short_name)
            except:
                pass

            try:
                width = config.NEWSCENTER_IMAGE_WIDTH
            except:
                width = getattr(settings, 'NEWSCENTER_IMAGE_WIDTH', 800)

            try:
                height = config.NEWSCENTER_IMAGE_HEIGHT
            except:
                height = getattr(settings, 'NEWSCENTER_IMAGE_HEIGHT', 600)

            try:
                imquality = config.NEWSCENTER_IMAGE_QUALITY
            except:
                imquality = getattr(settings, 'NEWSCENTER_IMAGE_QUALITY', 100)

            size = (width, height)
            image.thumbnail(size, PIL.Image.ANTIALIAS)
            image.save(filename, quality=imquality)
