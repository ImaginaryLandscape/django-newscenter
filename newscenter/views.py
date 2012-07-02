from django import http, shortcuts, template
from django.conf import settings
from newscenter import models
from django.views.generic import date_based
from django.contrib.sites.models import Site
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import get_object_or_404

def article_detail(request, newsroom, year, month, slug):
    request,
    year = year,
    month = month,
    article = get_object_or_404(models.Article.objects.get_published(), slug__exact=slug)
    newsroom = article.newsroom
    theme = newsroom.theme
    return shortcuts.render_to_response(
        'newscenter/article_detail.html', locals(),
        context_instance=template.RequestContext(request))

def archive_year(request, newsroom, year):
    room = models.Newsroom.objects.get(slug__exact=newsroom)
    return date_based.archive_year(
        request,
        year = year,
        date_field = 'release_date',
        make_object_list = True,        
        extra_context = {'newsroom': room},
        queryset = models.Article.objects.get_published().filter(
            newsroom__slug=newsroom)
    )
def archive_month(request, newsroom, year, month):
    room = models.Newsroom.objects.get(slug__exact=newsroom)
    return date_based.archive_month(
        request,
        year = year,
        month = month,
        date_field = 'release_date',
        extra_context = {'newsroom': room},
        queryset = models.Article.objects.get_published().filter(
            newsroom__slug=newsroom)
    )

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
    theme = newsroom.theme
    featured_list = newsroom.articles.get_featured()
    article_list = newsroom.articles.get_published()
    if theme == 'standard':
        paginator = Paginator(article_list, 10)
        page = int(request.GET.get('page', '1'))
        article_list = paginator.page(page)

    return shortcuts.render_to_response(
        'newscenter/newsroom_'+theme+'.html', locals(),
        context_instance=template.RequestContext(request))
