from django.db import models
from django_summernote.fields import SummernoteTextField


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = SummernoteTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes_count = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.title


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes', to_field='slug')
