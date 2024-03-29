from django import shortcuts, template
from django.shortcuts import render
from django.conf import settings
from django.views.generic import (YearArchiveView, MonthArchiveView,
    DetailView, RedirectView)
from django.views.generic.list import ListView
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404, render
try:
    from django.urls import reverse
except:
    from django.core.urlresolvers import reverse
from django.contrib.auth.views import redirect_to_login
from urllib.parse import quote
from newscenter import models
import random

class NewsroomIndex(ListView):
    model = models.Newsroom

    def get_context_data(self, *args, **kwargs):
        ctx = super(NewsroomIndex, self).get_context_data(*args, **kwargs)
        website = self.kwargs.get('website', None)
        ctx['website'] = website
        return ctx

    def get_queryset(self):
        if self.kwargs.get('website'):
            return models.Newsroom.objects.filter(
                website__short_name=self.kwargs.get('website')
            )
        else:
            return models.Newsroom.objects.all()

if 'light_draft' in settings.INSTALLED_APPS:
    from light_draft.views import BaseDraftView
    DetailView = BaseDraftView


class ArticleDetail(DetailView):
    model = models.Article

    def get_context_data(self, *args, **kwargs):
        ctx = super(ArticleDetail, self).get_context_data(*args, **kwargs)

        if hasattr(self.request, 'toolbar'):
            try:
                from cms.cms_toolbars import ADMIN_MENU_IDENTIFIER
            except:
                from cms.cms_toolbar import ADMIN_MENU_IDENTIFIER
            admin_menu = self.request.toolbar.get_or_create_menu(
                ADMIN_MENU_IDENTIFIER,
                _('Apps'))
            menu = admin_menu.get_or_create_menu(
                'newscenter-menu',
                _('Newscenter ...'))
            menu.add_break()
            menu.add_modal_item(_('Change this Article'), url=reverse(
                'admin:newscenter_article_change', args=[self.object.id]))

        ctx['newsroom'] = self.object.newsroom
        return ctx

    def get(self, request, *args, **kwargs):
        if 'hash' not in self.request.GET:
            self.object = get_object_or_404(
                models.Article.objects.get_published(),
                slug__exact=self.kwargs.get('slug'),
                newsroom__slug__exact=self.kwargs.get('newsroom'))
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        if ((self.object.private or self.object.newsroom.private) and not
            request.user.is_authenticated):
            return redirect_to_login(quote(request.get_full_path()),
                settings.LOGIN_URL)
        else:
            return self.render_to_response(context)


class ArchiveYear(YearArchiveView):
    context_object_name = 'article_list'
    model = models.Article
    date_field = 'release_date'
    make_object_list = True

    def get_queryset(self):
        try:
            return models.Article.objects.get_published().filter(
                newsroom__slug=self.kwargs['newsroom'],
                newsroom__website__short_name=self.kwargs.get('website', None))
        except:
            return models.Article.objects.get_published().filter(
                newsroom__slug=self.kwargs['newsroom'])

    def get_context_data(self, *args, **kwargs):
        ctx = super(ArchiveYear, self).get_context_data(*args, **kwargs)
        try:
            newsroom = get_object_or_404(
                models.Newsroom,
                slug__exact=self.kwargs['newsroom'],
                website__short_name__exact=self.kwargs.get('website', None))
        except:
            newsroom = get_object_or_404(
                models.Newsroom,
                slug__exact=self.kwargs['newsroom'])
        ctx['newsroom'] = newsroom
        return ctx

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a template rendered with the given context.
        """
        if context['newsroom'].private  and not self.request.user.is_authenticated:
            return redirect_to_login(quote(self.request.get_full_path()), 
                settings.LOGIN_URL)
        else:
            return self.response_class(
                request = self.request,
                template = self.get_template_names(),
                context = context,
                **response_kwargs
            )

class ArchiveMonth(MonthArchiveView):
    context_object_name = 'article_list'
    model = models.Article
    date_field = 'release_date'
    make_object_list = True

    def get_queryset(self):
        try:
            return models.Article.objects.get_published().filter(
                newsroom__slug=self.kwargs['newsroom'],
                newsroom__website__short_name=self.kwargs.get('website', None))
        except:
            return models.Article.objects.get_published().filter(
                newsroom__slug=self.kwargs['newsroom'])

    def get_context_data(self, *args, **kwargs):
        ctx = super(ArchiveMonth, self).get_context_data(*args, **kwargs)
        try:
            newsroom = get_object_or_404(
                models.Newsroom,
                slug__exact=self.kwargs['newsroom'],
                website__short_name__exact=self.kwargs.get('website', None))
        except:
            newsroom = get_object_or_404(
                models.Newsroom,
                slug__exact=self.kwargs['newsroom'])

        ctx['newsroom'] = newsroom
        return ctx

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a template rendered with the given context.
        """
        if context['newsroom'].private  and not self.request.user.is_authenticated:
            return redirect_to_login(quote(self.request.get_full_path()),
                settings.LOGIN_URL)
        else:
            return self.response_class(
                request = self.request,
                template = self.get_template_names(),
                context = context,
                **response_kwargs
            )

class DayOfWeek(ListView):
    model = models.Article
    template_name = "newscenter/day_of_week.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super(DayOfWeek, self).get_context_data(*args, **kwargs)
        days = {'sun':'Sunday','mon':'Monday', 'tue':'Tuesday', 
                'wed':'Wednesday', 'thu':'Thursday','fri':'Friday',
                'sat':'Saturday'}
        dayofweek = days[self.kwargs['dayofweek']]
        newsroom = get_object_or_404(models.Newsroom,
            slug__exact=self.kwargs['newsroom'])
        ctx['dayofweek'] = dayofweek
        ctx['newsroom'] = newsroom
        return ctx

    def get_queryset(self):
        dayofweek = [0,'sun','mon','tue','wed','thu','fri','sat'].index(
            self.kwargs['dayofweek'])
        newsroom = get_object_or_404(models.Newsroom,
            slug__exact=self.kwargs['newsroom'])
        articles = newsroom.articles.get_published().filter(
            release_date__week_day=dayofweek)

        return articles


def category_detail(request, slug):
    category = get_object_or_404(models.Category, slug__exact=slug)
    article_list = category.articles.get_published()
    return render(request, 'newscenter/category_detail.html',
        {'category': category, 'article_list': article_list,})


def newsroom_detail(request, slug, website=None, *args, **kwargs):
    site = Site.objects.get_current()
    if 'site_config.backend.model_backend' in settings.INSTALLED_APPS:
        model_kwargs = {'slug__exact': slug,
                        'website__short_name__exact': website}
    else:
        model_kwargs = {'slug__exact': slug}
    newsroom = get_object_or_404(models.Newsroom, **model_kwargs)
    article_list = newsroom.articles.get_published()

    if newsroom.private and not request.user.is_authenticated:
        return redirect_to_login(quote(request.get_full_path()),
            settings.LOGIN_URL)
    else:
        return render(request, 'newscenter/newsroom.html', locals())

def dual_newsrooms(request, slug1, slug2):
    from django.core.paginator import Paginator
    newsroom1 = get_object_or_404(models.Newsroom, slug__exact=slug1)
    newsroom2 = get_object_or_404(models.Newsroom, slug__exact=slug2)
    article1 = newsroom1.articles.get_published().order_by('release_date')
    article2 = newsroom2.articles.get_published().order_by('release_date')
    paginator1 = Paginator(article1, 1)
    paginator2 = Paginator(article2, 1)
    page = int(request.GET.get('page', '1'))
    article1 = paginator1.page(page)
    article2 = paginator2.page(page)

    return render(request, 'newscenter/dual_newsrooms.html', locals())

class NewsroomLatest(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        newsroom = get_object_or_404(
            models.Newsroom,
            slug__exact=self.kwargs['newsroom'])
        article = newsroom.articles.get_published()[0]
        return article.get_absolute_url()


class NewsroomRandom(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        newsroom = get_object_or_404(
            models.Newsroom,
            slug__exact=self.kwargs['newsroom'])
        articles = newsroom.articles.get_published()
        category = self.request.GET.get('category', '')
        if category:
            articles = articles.filter(categories__slug=category)
        article = random.choice(articles)
        return article.get_absolute_url()

class RandomFeatured(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        include_newsrooms = getattr(settings, 'NEWSCENTER_INCLUDE_RANDOM_FEATURED_NEWSROOMS', [])
        featured = models.Article.objects.get_featured().filter(newsroom__slug__in=include_newsrooms)
        article = random.choice(featured)
        return article.get_absolute_url()
