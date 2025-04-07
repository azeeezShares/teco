from . import views
from django.urls import path

urlpatterns = [
    path('blog/', views.PostList.as_view(), name='blog_homeview'),
    path('blog/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('blog/tag/<str:tag>/', views.TagList.as_view(), name='tag_list'),
]