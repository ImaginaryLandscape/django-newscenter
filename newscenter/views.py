from django import http, shortcuts, template
from django.conf import settings
from django.views.generic import YearArchiveView, MonthArchiveView
from django.contrib.sites.models import Site
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import get_object_or_404

from newscenter import models

def article_detail(request, newsroom, year, month, slug):
    request,
    year = year,
    month = month,
    article = get_object_or_404(models.Article.objects.get_published(), 
        slug__exact=slug, newsroom__slug__exact=newsroom)
    newsroom = article.newsroom
    return shortcuts.render_to_response(
        'newscenter/article_detail.html', locals(),
        context_instance=template.RequestContext(request))

class ArchiveYear(YearArchiveView):
    model = models.Article
    date_field = 'release_date'
    make_object_list = True

    def get_queryset(self):
        return models.Article.objects.get_published().filter(
            newsroom__slug=self.kwargs['newsroom']
        )

    def get_context_data(self, *args, **kwargs):
        ctx = super(ArchiveYear, self).get_context_data(*args, **kwargs)
        newsroom = get_object_or_404(models.Newsroom, 
            slug__exact=self.kwargs['newsroom'])
        ctx['newsroom'] = newsroom
        return ctx        


class ArchiveMonth(MonthArchiveView):
    model = models.Article
    date_field = 'release_date'
    make_object_list = True

    def get_queryset(self):
        return models.Article.objects.get_published().filter(
            newsroom__slug=self.kwargs['newsroom']
        )

    def get_context_data(self, *args, **kwargs):
        ctx = super(ArchiveMonth, self).get_context_data(*args, **kwargs)
        newsroom = get_object_or_404(models.Newsroom, 
            slug__exact=self.kwargs['newsroom'])        
        ctx['newsroom'] = newsroom
        return ctx        

def category_detail(request, slug):
    category = models.Category.objects.get(slug__exact=slug)
    article_list = category.articles.get_published()
    return shortcuts.render_to_response(
        'newscenter/category_detail.html', 
        {'category': category, 'article_list': article_list,},
        context_instance=template.RequestContext(request))

def newsroom_detail(request, slug):
    site = Site.objects.get_current()
    newsroom = get_object_or_404(models.Newsroom, slug__exact=slug)
    article_list = newsroom.articles.get_published()
    paginator = Paginator(article_list, 10)
    page = int(request.GET.get('page', '1'))
    article_list = paginator.page(page)

    return shortcuts.render_to_response(
        'newscenter/newsroom.html', locals(),
        context_instance=template.RequestContext(request))
