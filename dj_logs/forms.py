from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'text']
        labels = {
            # 'name': '主题名字',
            'text': 'SUMMARY'
            }
        widgets = {'text': forms.Textarea(attrs={'cols': 50})}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 50})}