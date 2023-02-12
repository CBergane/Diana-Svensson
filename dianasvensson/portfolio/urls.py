from django.urls import path, include
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('summernote/', include('django_summernote.urls')),
]
