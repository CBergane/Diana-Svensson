from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Post, Like
from .forms import PostForm

def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.likes += 1
            post.save()
            return redirect('display_posts')
    return render(request, 'portfolio/create_post.html', {'form': form})



def delete_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        post.delete()
    except Post.DoesNotExist:
        messages.error(request, 'Post not found.')
    return redirect('display_posts')


def update_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts')
    else:
        form = PostForm(instance=post)
    return render(request, 'update_post.html', {'form': form})

def display_posts(request):
    posts = Post.objects.all()
    return render(request, 'portfolio/post_list.html', {'posts': posts})

def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.likes += 1
    post.save()
    return redirect('posts')

def unlike_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.likes -= 1
    post.save()
    return redirect('posts')
