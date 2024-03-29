try:
    from cms.wizards.wizard_base import Wizard
    from cms.wizards.wizard_pool import wizard_pool
    from cms.wizards.forms import BaseFormMixin    

    from django import forms
    from django.forms import widgets

    from django.conf import settings

    from .models import Article

    class ArticleWizardForm(forms.ModelForm):
        if 'djangocms_text_ckeditor' in settings.INSTALLED_APPS:
            from djangocms_text_ckeditor.widgets import TextEditorWidget
            body = forms.CharField(widget=TextEditorWidget())

        class Meta:
            model = Article
            fields = ['title', 'slug', 'release_date', 'newsroom', 'body']

    class ArticleWizard(Wizard):
        pass

    newscenter_wizard = ArticleWizard(
        title="New Article",
        weight=200,
        form=ArticleWizardForm,
        model=Article,
        description="Create a new article in Newscenter",
    )

    wizard_pool.register(newscenter_wizard)

except ImportError:
    # For django CMS version not supporting wizards just ignore this file
    pass    
