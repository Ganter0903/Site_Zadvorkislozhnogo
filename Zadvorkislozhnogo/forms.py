from django import forms
from .models import Story, Poem, Audiobook

class BaseContentForm(forms.ModelForm):
    class Meta:
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }

class StoryForm(BaseContentForm):
    class Meta(BaseContentForm.Meta):
        model = Story

class PoemForm(BaseContentForm):
    class Meta(BaseContentForm.Meta):
        model = Poem

class AudiobookForm(BaseContentForm):
    class Meta(BaseContentForm.Meta):
        model = Audiobook
        fields = BaseContentForm.Meta.fields + ['audio_file']
        widgets = {
            **BaseContentForm.Meta.widgets,
            'audio_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
