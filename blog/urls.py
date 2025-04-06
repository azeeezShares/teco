from . import views
from django.urls import path

urlpatterns = [
    path('blog/', views.PostList.as_view(), name='blog_homeview'),
    path("editor/", views.PageEdit.as_view(), name="editor"),
    path('blog/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]