from django.contrib import admin
from django.conf import settings
from newscenter import models, widgets, forms

class ImageInline(admin.StackedInline):
    model = models.Image
    extra = 1

class ArticleInline(admin.StackedInline):
    model = models.Article
    extra = 0

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone',)
    search_fields = ('name', 'email', 'phone',)

class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

class NewsroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'website_short_name')
    prepopulated_fields = {'slug' : ('name',)}


model_admin = admin.ModelAdmin
if 'reversion' in settings.INSTALLED_APPS:
    from reversion.admin import VersionAdmin
    model_admin = VersionAdmin

class ArticleAdmin(model_admin):
    inlines = [
        ImageInline,
    ]
    list_display = ('title', 'release_date', 'expire_date', 'active', 
        'featured','newsroom',)
    list_editable = ('active', 'featured','newsroom',)
    search_fields = ['title', 'body', 'teaser',]
    list_filter = ('contacts', 'release_date', 'expire_date', 'newsroom', 'active', 
        'featured', 'categories',)
    prepopulated_fields = {'slug' : ('title',)}
    date_heirarchy = 'release_date'
    filter_horizontal = ('categories',)
    fieldsets = (
        (None, {'fields': (('title', 'slug'), ('newsroom', 'active', 
                'featured'), 'categories', ('contacts', 'location'), 
                'teaser', 'body', ('release_date', 'expire_date'),)}),
    )
    form = forms.ArticleAdminModelForm

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ['title',]
    prepopulated_fields = {'slug' : ('title',)}
    fieldsets = (
        ('Category', {'fields': ('title', 'slug')}),
    )

admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Contact, ContactAdmin)
admin.site.register(models.Newsroom, NewsroomAdmin)
admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Category, CategoryAdmin)
