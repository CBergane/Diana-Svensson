from django.urls import path
from . import views
from .views import TimelineView, ExperienceCreateView, EducationCreateView

urlpatterns = [
    path('', views.display_posts, name='display_posts'),
    path('posts/', views.display_posts, name='display_posts'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('posts/<int:post_id>/update/', views.update_post, name='update_post'),
    path('posts/<int:post_id>/like/', views.like_post, name='like_post'),
    path('posts/<int:post_id>/unlike/', views.unlike_post, name='unlike_post'),
    path('timeline/', TimelineView.as_view(), name='timeline'),
    path('add_experience/', ExperienceCreateView.as_view(), name='add_experience'),
    path('add_education/', EducationCreateView.as_view(), name='add_education'),
]
