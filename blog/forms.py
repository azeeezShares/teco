from django import forms
from froala_editor.widgets import FroalaEditor
from .models import Post

class PageForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', ]
        widgets = {
            'content': FroalaEditor(),
        }