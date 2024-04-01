from django.shortcuts import render
from .models import Post, PostComment, PostLike, CommentLike
from .serializers import PostSerializer, PostCommentSerializer, CommentLikeSerializer, PostLikeSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView




class PostListAPIView(ListAPIView):
    
    queryset = Post.objects.all()
    serializer_class = PostSerializer



