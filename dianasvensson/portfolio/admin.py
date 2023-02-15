from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'created_at')
    search_fields = ['title', 'content']
    list_filter = ['created_at']
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)