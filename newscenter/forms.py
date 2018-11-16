from django import forms
try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models import get_model
from django.conf import settings
from newscenter.widgets import SmallTextField

REQUIRE_TEASER = getattr(settings, 'NEWSCENTER_REQUIRE_TEASER', False)
TITLE_MAXLENGTH = getattr(settings, 'NEWSCENTER_TITLE_MAXLENGTH', '')

class ArticleAdminModelForm(forms.ModelForm):
    if 'djangocms_text_ckeditor' in settings.INSTALLED_APPS:
        from djangocms_text_ckeditor.widgets import TextEditorWidget
        body = forms.CharField(widget=TextEditorWidget())
    elif 'tinymce' in settings.INSTALLED_APPS:
        from tinymce.widgets import TinyMCE
        body = forms.CharField(widget=TinyMCE())
    teaser = forms.CharField(required=REQUIRE_TEASER, widget=SmallTextField())
    title = forms.CharField(widget=forms.TextInput(
        attrs={'maxlength': TITLE_MAXLENGTH}))

    class Meta:
        model = get_model('newscenter', 'article')
        exclude = []
