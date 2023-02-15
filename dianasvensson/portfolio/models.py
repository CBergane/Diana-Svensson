from django.db import models
from django.utils.text import slugify
import itertools
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = orig = slugify(self.title)
            for i in itertools.count(1):
                if not Post.objects.filter(slug=self.slug).exists():
                    break
                self.slug = f"{orig}-{i}"
        super(Post, self).save(*args, **kwargs)




class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes', to_field='slug')
