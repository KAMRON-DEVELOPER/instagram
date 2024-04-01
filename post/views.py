from django.shortcuts import render
from .models import Post, PostComment, PostLike, CommentLike
from .serializers import PostSerializer, PostCommentSerializer, CommentLikeSerializer, PostLikeSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework import permissions
from shared.pagination import CustomPagination




class PostListAPIView(ListAPIView):
    
    permission_classes = [permissions.AllowAny,]
    # queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = CustomPagination()
    
    def get_queryset(self):
        return Post.objects.all()
    


class PosCreateAPIView(CreateAPIView):
    
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
        
        
class PostListCreateAPIView(ListCreateAPIView):
    
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = PostSerializer
    pagination_class = CustomPagination()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class PostRetrieveAPIView(RetrieveUpdateDestroyAPIView):

    permission_classes = [permissions.AllowAny,]
    queryset = Post.objects.all()
    serializer_class = PostSerializer





