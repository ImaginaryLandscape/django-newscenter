from django import forms
from django.conf import settings
from django.db.models import get_model
from newscenter.widgets import SmallTextField

class ArticleAdminModelForm(forms.ModelForm):
    if 'djangocms_text_ckeditor' in settings.INSTALLED_APPS:
        from djangocms_text_ckeditor.widgets import TextEditorWidget
        body = forms.CharField(widget=TextEditorWidget())
    elif 'tinymce' in settings.INSTALLED_APPS:
        from tinymce.widgets import TinyMCE
        body = forms.CharField(widget=TinyMCE())
    teaser = forms.CharField(required=False, widget=SmallTextField())

    class Meta:
        model = get_model('newscenter', 'article')

