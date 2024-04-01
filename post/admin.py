from django.contrib import admin
from .models import Post, PostComment, PostLike, CommentLike

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_time']


class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_time']
    

class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_time']


class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ['author', 'comment', 'created_time']
    
    
admin.site.register(Post, PostAdmin)
admin.site.register(PostComment, PostCommentAdmin)
admin.site.register(PostLike, PostLikeAdmin)
admin.site.register(CommentLike, CommentLikeAdmin)
