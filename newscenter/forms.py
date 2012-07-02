from django import forms
from django.db.models import get_model
from newscenter import widgets

class ArticleAdminModelForm(forms.ModelForm):
    body = forms.CharField(widget=widgets.TinyMCEWidget())
    teaser = forms.CharField(required=False, widget=widgets.SmallTextField())

    class Meta:
        model = get_model('newscenter', 'article')

