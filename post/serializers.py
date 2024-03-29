from rest_framework import serializers

from users.models import User
from .models import Post, PostComment, PostLike, CommentLike



class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'user_gender']



class PostSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)
    post_likes_count = serializers.SerializerMethodField('get_post_likes_count')
    post_comments_count = serializers.SerializerMethodField('get_post_comments_count')
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'body', 'post_image', 'created_time', 'post_likes_count', 'post_comments_count']

    def get_post_likes_count(self, obj):
        return obj.likes.count()
    
    def get_post_comments_count(self, obj):
        return obj.comments.count()




