from django import forms

from .models import News, Subscribe


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'text']


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ['user', 'subscribe']
        widgets = {'user': forms.HiddenInput(),
                   'subscribe': forms.HiddenInput()}
