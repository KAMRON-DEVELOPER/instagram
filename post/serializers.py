from rest_framework import serializers
from .models import Post, PostComment, PostLike, CommentLike




class PostSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(~)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'body', 'post_image', 'created_time']


