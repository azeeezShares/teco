from django.db import models
from django.contrib.auth.models import User
from account.models import CustomUser
from froala_editor.fields import FroalaField

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blog_posts')
    # cover image 2240x1260
    image = models.ImageField(upload_to='uploads/blog-thumbnails/', default='static/defaults/default.jpg')
    updated_on = models.DateTimeField(auto_now= True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    content = FroalaField()

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
  