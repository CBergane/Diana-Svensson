from django.shortcuts import render
from .models import Post, Like


def post_list(request):
    posts = Post.objects.all()
    if request.method == 'POST':
        post_slug = request.POST.get('post_slug')
        post = Post.objects.get(slug=post_slug)
        post.likes += 1
        post.save()
        Like.objects.create(post=post)
    return render(request, 'portfolio/post_list.html', {'posts': posts})
    
    