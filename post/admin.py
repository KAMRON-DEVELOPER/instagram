from django.contrib import admin
from .models import Post, PostComment, PostLike, CommentLike

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_time']


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_time']