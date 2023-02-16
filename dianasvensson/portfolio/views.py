from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import TemplateView, CreateView
from django.urls import reverse
from .models import Post, Like, Education, Experience
from .forms import PostForm, ExperienceForm, EducationForm

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
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 5) # Show 5 posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'portfolio/post_list.html', {'posts': posts})


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'portfolio/post_detail.html', {'post': post})


def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.likes += 1
    post.save()
    next_url = request.GET.get('next', 'display_posts')
    return redirect(reverse(next_url))


def unlike_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.likes -= 1
    post.save()
    return redirect('display_posts')


class TimelineView(TemplateView):
    template_name = 'portfolio/timeline.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['education'] = Education.objects.order_by('-start_date')
        context['experience'] = Experience.objects.order_by('-start_date')
        return context
    

class ExperienceCreateView(CreateView):
    model = Experience
    form_class = ExperienceForm
    template_name = 'portfolio/add_experience.html'

    def form_valid(self, form):
        experience = form.save(commit=False)
        experience.user = self.request.user
        experience.save()
        return redirect('timeline')
    

class EducationCreateView(CreateView):
    model = Education
    form_class = EducationForm
    template_name = 'portfolio/add_education.html'

    def form_valid(self, form):
        education = form.save(commit=False)
        education.user = self.request.user
        education.save()
        return redirect('timeline')