from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Post

class PageForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'status', 'content', 'image', 'summary', 'tag']
        labels = {
            'title': 'Title',
            'slug': 'Slug',
            'status': 'Status',
            'content': 'Content',
            'image': 'Image',
            'summary': 'Summary',
            'tag': 'Tags'
        }
        help_texts = {
            'title': 'Enter the title of the post',
            'slug': 'Enter a URL-friendly slug',
            'status': 'Select the status of the post',
            'content': 'Write the content of the post',
            'image': 'Upload an image for the post',
            'summary': 'Write a short summary of the post',
            'tag': 'Select tags for the post'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 text-sm font-normal shadow-xs text-gray-900 bg-transparent border border-gray-300 rounded-full placeholder-gray-400 focus:outline-none leading-relaxed focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Enter title',
                "id": "title_field",
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'URL-friendly slug',
                "id": "slug_field",
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'content': CKEditor5Widget(config_name='extends'),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full file:px-4 file:py-2 file:border-0 file:rounded-lg file:bg-blue-600 file:text-white'
            }),
            'tag': forms.CheckboxSelectMultiple(attrs={
                # 'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Write a short summary of the post',
                'rows': 3,
                "id": "summary_field",
            }),
        }
