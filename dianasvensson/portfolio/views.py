from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import TemplateView, CreateView
from django.urls import reverse
from .models import Post, Education, Experience
from .forms import PostForm, ExperienceForm, EducationForm

def create_post(request):
    """
    A view function that handles creating a new post.

    Args:
        request: A HTTP request object that contains information about the request.

    Returns:
        A HTTP response object that renders the 'portfolio/create_post.html' template with a form to create a new post.

        If the form is submitted with valid data, the post is created and the user is redirected to the 'display_posts' view.
    """
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
    """
    A view function that handles deleting a post with the given post_id.

    Args:
        request: A HTTP request object that contains information about the request.
        post_id: An integer representing the id of the post to be deleted.

    Returns:
        A HTTP response object that redirects the user to the 'display_posts' view after deleting the post.

        If the post with the given post_id does not exist, an error message is displayed and the user is redirected to the 'display_posts' view.
    """
    try:
        post = Post.objects.get(id=post_id)
        post.delete()
    except Post.DoesNotExist:
        messages.error(request, 'Post not found.')
    return redirect('display_posts')


def update_post(request, post_id):
    """
    A view function that handles updating a post with the given post_id.

    Args:
        request: A HTTP request object that contains information about the request.
        post_id: An integer representing the id of the post to be updated.

    Returns:
        A HTTP response object that renders the 'portfolio/update_post.html' template with a form to update the post.

        If the form is submitted with valid data, the post is updated and the user is redirected to the 'posts' view.
    """
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
    """
    A view function that handles displaying all posts.

    Args:
        request: A HTTP request object that contains information about the request.

    Returns:
        A HTTP response object that renders the 'portfolio/post_list.html' template with a list of all posts.

        The posts are displayed 5 at a time using pagination.
    """
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 5) # Show 5 posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'portfolio/post_list.html', {'posts': posts})


def post_detail(request, post_id):
    """
    A view function that handles displaying the details of a post with the given post_id.

    Args:
        request: A HTTP request object that contains information about the request.
        post_id: An integer representing the id of the post to be displayed.

    Returns:
        A HTTP response object that renders the 'portfolio/post_detail.html' template with the details of the post with the given post_id.
    """
    post = Post.objects.get(id=post_id)
    return render(request, 'portfolio/post_detail.html', {'post': post})


def like_post(request, post_id):
    """
    Increases the like count for the post with the given ID by 1.
    If a 'next' parameter is included in the request's GET data,
    the user is redirected to that URL; otherwise, the user is
    redirected to the 'display_posts' URL.

    Args:
    - request: The HTTP request object.
    - post_id: The ID of the post to like.

    Returns:
    - A redirect response to the specified URL.
    """
    post = get_object_or_404(Post, id=post_id)
    post.likes += 1
    post.save()
    next_url = request.GET.get('next', 'display_posts')
    return redirect(reverse(next_url))


def unlike_post(request, post_id):
    """
    Decreases the like count for the post with the given ID by 1.

    Args:
    - request: The HTTP request object.
    - post_id: The ID of the post to unlike.

    Returns:
    - A redirect response to the 'display_posts' URL.
    """
    post = Post.objects.get(id=post_id)
    post.likes -= 1
    post.save()
    return redirect('display_posts')


class TimelineView(TemplateView):
    """
    Renders the 'timeline.html' template, which displays the user's
    education and experience information in reverse chronological order.

    Methods:
    - get_context_data: Returns a dictionary containing the user's
      education and experience information.
    """
    template_name = 'portfolio/timeline.html'
    
    def get_context_data(self, **kwargs):
        """
        Returns a dictionary containing the user's education and experience
        information, sorted by start date in reverse chronological order.

        Args:
        - **kwargs: Any additional keyword arguments.

        Returns:
        - A dictionary containing the user's education and experience
          information, sorted by start date in reverse chronological order.
        """
        context = super().get_context_data(**kwargs)
        context['education'] = Education.objects.order_by('-start_date')
        context['experience'] = Experience.objects.order_by('-start_date')
        return context
    

class ExperienceCreateView(CreateView):
    """
    Renders the 'add_experience.html' template, which allows the user
    to add a new experience entry.

    Attributes:
    - model: The Experience model class.
    - form_class: The form class to use for creating a new experience.
    - template_name: The name of the template to render.

    Methods:
    - form_valid: Saves the new experience entry and redirects the user
      to the 'timeline' URL.
    """
    model = Experience
    form_class = ExperienceForm
    template_name = 'portfolio/add_experience.html'

    def form_valid(self, form):
        """
        Saves the new experience entry and redirects the user to the
        'timeline' URL.

        Args:
        - form: The form object containing the user's input.

        Returns:
        - A redirect response to the 'timeline' URL.
        """
        experience = form.save(commit=False)
        experience.user = self.request.user
        experience.save()
        return redirect('timeline')
    

class EducationCreateView(CreateView):
    """
    A class-based view that handles the creation of new Education objects.

    Inherits from Django's built-in `CreateView` class.

    Attributes:
    - model: The Django model that the form should create instances of.
    - form_class: The form that should be used to create instances of the model.
    - template_name: The name of the template to render when the form is displayed.

    Methods:
    - form_valid(form): Overrides the default behavior to add the user to the new
                        education instance and then redirect to the timeline view.

    """
    model = Education
    form_class = EducationForm
    template_name = 'portfolio/add_education.html'

    def form_valid(self, form):
        """
        Saves the form and associates the new education instance with the current user.

        Args:
        - form: The form to save.

        Returns:
        A redirect to the timeline view.
        """
        education = form.save(commit=False)
        education.user = self.request.user
        education.save()
        return redirect('timeline')
