from django import forms
from .models import Story, Poem, Audiobook, User, Blog

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

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'surname', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.TextInput(attrs={'class': 'form-control'}),
        }