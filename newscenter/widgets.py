from django import forms
from django.utils.safestring import mark_safe


class SmallTextField(forms.Textarea):
    def render(self, name, value, attrs=None):
        self.attrs = {'rows': '3', 'cols': '50'}
        output = [super(SmallTextField, self).render(name, value, attrs)]
        return mark_safe(u''.join(output))
