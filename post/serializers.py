from rest_framework import serializers
from .models import Post, PostComment, PostLike, CommentLike




class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ['']


