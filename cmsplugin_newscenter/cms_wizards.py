try:
    from cms import __version__ as cms_version
    from cms.wizards.wizard_base import Wizard

    from django import forms

    from django.conf import settings

    from newscenter.models import Article

    class ArticleWizardForm(forms.ModelForm):
        if 'djangocms_text_ckeditor' in settings.INSTALLED_APPS:
            from djangocms_text_ckeditor.widgets import TextEditorWidget
            body = forms.CharField(widget=TextEditorWidget())

        class Meta:
            model = Article
            fields = ['title', 'release_date', 'newsroom', 'body', 'feeds']

    class ArticleWizard(Wizard):
        pass

    newscenter_wizard = ArticleWizard(
        title="New Article",
        weight=200,
        form=ArticleWizardForm,
        model=Article,
        edit_mode_on_success=False,
        description="Create a new article in Newscenter",
    )

    # django CMS 4+ registers wizards through cms_config.py
    if int(cms_version.split('.')[0]) < 4:
        from cms.wizards.wizard_pool import wizard_pool
        wizard_pool.register(newscenter_wizard)

except ImportError:
    # For django CMS version not supporting wizards just ignore this file
    pass
