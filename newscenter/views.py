from django import http, shortcuts, template
from django.conf import settings
from django.views.generic import YearArchiveView, MonthArchiveView
from django.contrib.sites.models import Site
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from newscenter import models

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
        return models.Article.objects.get_published().filter(
            newsroom__slug=self.kwargs['newsroom'], 
            newsroom__website_short_name=self.kwargs.get('website', '')
        )

    def get_context_data(self, *args, **kwargs):
        ctx = super(ArchiveYear, self).get_context_data(*args, **kwargs)
        newsroom = get_object_or_404(models.Newsroom, 
            slug__exact=self.kwargs['newsroom'], 
            website_short_name__exact=self.kwargs.get('website', '')
        )
        ctx['newsroom'] = newsroom
        return ctx        


class ArchiveMonth(MonthArchiveView):
    model = models.Article
    date_field = 'release_date'
    make_object_list = True

    def get_queryset(self):
        return models.Article.objects.get_published().filter(
            newsroom__slug=self.kwargs['newsroom'],
            newsroom__website_short_name=self.kwargs.get('website', '')
        )

    def get_context_data(self, *args, **kwargs):
        ctx = super(ArchiveMonth, self).get_context_data(*args, **kwargs)
        newsroom = get_object_or_404(models.Newsroom, 
            slug__exact=self.kwargs['newsroom'],
            website_short_name__exact=self.kwargs.get('website', '')
        )
        ctx['newsroom'] = newsroom
        return ctx        

def category_detail(request, slug):
    category = models.Category.objects.get(slug__exact=slug)
    article_list = category.articles.get_published()
    return shortcuts.render_to_response(
        'newscenter/category_detail.html', 
        {'category': category, 'article_list': article_list,},
        context_instance=template.RequestContext(request))

def newsroom_detail(request, slug, website='', *args, **kwargs):
    site = Site.objects.get_current()
    model_kwargs={ 'slug__exact':slug, 'website_short_name__exact':website}
    newsroom = get_object_or_404(models.Newsroom, **model_kwargs)
    article_list = newsroom.articles.get_published()
    paginator = Paginator(article_list, 10)
    page = int(request.GET.get('page', '1'))
    article_list = paginator.page(page)

    return shortcuts.render_to_response(
        'newscenter/newsroom.html', locals(),
        context_instance=template.RequestContext(request))
