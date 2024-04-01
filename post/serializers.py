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
    did_i_like = serializers.SerializerMethodField('get_did_i_like')
    comment_likes_count = serializers.SerializerMethodField('get_comment_likes_count')
    
    class Meta:
        model = PostComment
        fields = ['id', 'author', 'comment', 'parent', 'created_time', 'replies', 'get_did_i_like', 'get_comment_likes_count']

    def get_replies(self, obj):
        if obj.children.exists():
            serializers = self.__class__(obj.cildren.all(), many=True, context=self.context) # bu orqali CommentSerializerni o'ziga murojat etamiz va undan barcha likelarni olamiz.
            return serializers.data
        else:
            return None
    
    def get_did_i_like(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return user.likes.filter(author=user).exists()
        else:
            return False
    
    @staticmethod
    def get_comment_likes_count(obj):
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




