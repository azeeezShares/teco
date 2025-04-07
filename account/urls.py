from django.urls import path
from . import views
import blog.views as blog_views

ENDPOINT = 'QDyDjq'

urlpatterns = [
    path(f'{ENDPOINT}/', views.AdminLogin.as_view(), name='admin_login'),
    path(f'{ENDPOINT}/view/', views.AdminView.as_view(), name='admin_view'),
    # path('{ENDPOINT}/booking/<int:pk>/', views.booking_detail.as_view(), name='booking_detail'),
    
    # path for blog
    path(f'{ENDPOINT}/blog/', blog_views.AdminPostList.as_view(), name='admin_blogview'),
    # path for blog edit
    path(f'{ENDPOINT}/blog/edit/', blog_views.AdminPostEdit.as_view(), name='admin_blog_edit'),
    # path for delete blog
    path(f'{ENDPOINT}/blog/delete/', blog_views.AdminPostDelete.as_view(), name='admin_blog_delete'),
    #path for create blog
    path(f'{ENDPOINT}/blog/create/', blog_views.AdminPostCreate.as_view(), name='admin_blog_create'),
]
