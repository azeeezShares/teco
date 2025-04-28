# blog/templatetags/button.py
from django import template

from blog.models import Post


register = template.Library()

@register.inclusion_tag('components/button.html')
def show_latest_posts(count=5):
    posts = Post.objects.order_by('-updated_on')[:count]
    return {'posts': posts}

@register.inclusion_tag("components/navbar.html")
def navbar():
    return {}

@register.inclusion_tag("components/change_language_button.html")
def change_language_button(id=0):
    return {"id":id}