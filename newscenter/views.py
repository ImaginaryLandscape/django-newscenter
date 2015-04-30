from django import http, shortcuts, template
from django.conf import settings
from django.views.generic import YearArchiveView, MonthArchiveView, DetailView
from django.views.generic.list import ListView
from django.contrib.sites.models import Site
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from newscenter import models

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
            from cms.cms_toolbar import ADMIN_MENU_IDENTIFIER      
            admin_menu = self.request.toolbar.get_or_create_menu(ADMIN_MENU_IDENTIFIER, 
                _('Apps'))
            menu = admin_menu.get_or_create_menu('newscenter-menu',
                _('Newscenter ...'))
            menu.add_break()        
            menu.add_modal_item(_('Change this Article'), url=reverse(
                'admin:newscenter_article_change', args=[self.object.id]))

        ctx['newsroom'] = self.object.newsroom
        return ctx

    def get(self, request, *args, **kwargs):
        if 'hash' not in self.request.GET:
            self.object = get_object_or_404(models.Article.objects.get_published(),
                slug__exact=self.kwargs.get('slug'), newsroom__slug__exact=self.kwargs.get('newsroom'))
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

def article_detail(request, newsroom, year, month, slug, website=None, template_name='', *args, **kwargs):
    request
    year = year
    month = month
    article = get_object_or_404(models.Article.objects.get_published(), 
        slug__exact=slug, newsroom__slug__exact=newsroom)
    newsroom = article.newsroom
    if hasattr(request, 'toolbar'):    
        from cms.cms_toolbar import ADMIN_MENU_IDENTIFIER      
        admin_menu = request.toolbar.get_or_create_menu(ADMIN_MENU_IDENTIFIER, 
            _('Apps'))
        menu = admin_menu.get_or_create_menu('newscenter-menu',
            _('Newscenter ...'))
        menu.add_break()        
        menu.add_modal_item(_('Change this Article'), url=reverse(
            'admin:newscenter_article_change', args=[article.id]))
    return shortcuts.render_to_response(
        template_name, locals(),
        context_instance=template.RequestContext(request))

class ArchiveYear(YearArchiveView):
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
            newsroom = get_object_or_404(models.Newsroom, 
                slug__exact=self.kwargs['newsroom'], 
                website__short_name__exact=self.kwargs.get('website', None))
        except:
            newsroom = get_object_or_404(models.Newsroom,
                slug__exact=self.kwargs['newsroom'])
        ctx['newsroom'] = newsroom
        return ctx        


class ArchiveMonth(MonthArchiveView):
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
            newsroom = get_object_or_404(models.Newsroom, 
                slug__exact=self.kwargs['newsroom'],
                website__short_name__exact=self.kwargs.get('website', None))
        except:
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

def newsroom_detail(request, slug, website=None, *args, **kwargs):
    site = Site.objects.get_current()
    if 'site_config.backend.model_backend' in settings.INSTALLED_APPS:
        model_kwargs={'slug__exact':slug, 'website__short_name__exact':website}
    else:
        model_kwargs={'slug__exact':slug}
    newsroom = get_object_or_404(models.Newsroom, **model_kwargs)
    article_list = newsroom.articles.get_published()
    paginator = Paginator(article_list, getattr(settings, 'NEWSCENTER_PAGINATE_BY', 10))
    page = int(request.GET.get('page', '1'))
    article_list = paginator.page(page)

    return shortcuts.render_to_response(
        'newscenter/newsroom.html', locals(),
        context_instance=template.RequestContext(request))
