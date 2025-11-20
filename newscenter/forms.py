from django import forms
from django.apps import apps
from django.conf import settings
from newscenter.widgets import SmallTextField

REQUIRE_TEASER = getattr(settings, 'NEWSCENTER_REQUIRE_TEASER', False)
TITLE_MAXLENGTH = getattr(settings, 'NEWSCENTER_TITLE_MAXLENGTH', 400)
TITLE_MINLENGTH = getattr(settings, 'NEWSCENTER_TITLE_MINLENGTH', 0)

class ArticleAdminModelForm(forms.ModelForm):
    if 'djangocms_text_ckeditor' in settings.INSTALLED_APPS:
        from djangocms_text_ckeditor.widgets import TextEditorWidget
        body = forms.CharField(widget=TextEditorWidget())
    elif 'tinymce' in settings.INSTALLED_APPS:
        from tinymce.widgets import TinyMCE
        body = forms.CharField(widget=TinyMCE())
    elif 'ckeditor' in settings.INSTALLED_APPS:
        from ckeditor.widgets import CKEditorWidget
        body = forms.CharField(widget=CKEditorWidget())
    teaser = forms.CharField(required=REQUIRE_TEASER, widget=SmallTextField())
    title = forms.CharField(max_length=TITLE_MAXLENGTH,
        min_length=TITLE_MINLENGTH,
        widget=forms.TextInput(attrs={'maxlength': TITLE_MAXLENGTH}))

    class Meta:
        model = apps.get_model('newscenter', 'article')
        exclude = []
