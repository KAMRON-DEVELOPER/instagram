from rest_framework import serializers

from users.models import User
from .models import Post, PostComment, PostLike, CommentLike



class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    
    class Meta:
        model = User
        fields = [ 'id','username', 'photo', 'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'user_gender']



class PostSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)
    post_likes_count = serializers.SerializerMethodField('get_post_likes_count')
    post_comments_count = serializers.SerializerMethodField('get_post_comments_count')
    did_i_like = serializers.SerializerMethodField('get_did_i_like')
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'body', 'post_image', 'created_time', 'post_likes_count', 'post_comments_count', 'did_i_like']

    extra_kwargs = {"image" : {"required" : False}}

    @staticmethod
    def get_post_likes_count(obj):
        return obj.likes.count()
    
    def get_post_comments_count(self, obj):
        return obj.comments.count()

    def get_did_i_like(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            try:
                like = PostLike.objects.get(post=obj, author=request.user)
                return True
            except PostLike.DoesNotExist:
                return False
        return False



class PostCommentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField('get_replies')
    me_liked = serializers.SerializerMethodField('get_me_liked')
    likes_count = serializers.SerializerMethodField('get_likes_count')

    class Meta:
        model = PostComment
        fields = [
            "id",
            "author",
            "comment",
            "post",
            "parent",
            "created_time",
            "replies",
            "me_liked",
            "likes_count",
          ]

    def get_replies(self, obj):
        if obj.children.exists():
            serializers = self.__class__(obj.children.all(), many=True, context=self.context)
            return serializers.data
        else:
            return None

    def get_me_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(author=user).exists()
        else:
            return False

    @staticmethod
    def get_likes_count(obj):
        return obj.likes.count()



class CommentLikeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = CommentLike
        fields = ['id', 'author', 'comment']



class PostLikeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = PostLike
        fields = ['id', 'author', 'post']




