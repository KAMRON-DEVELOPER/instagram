from django.urls import path

from .views import *




urlpatterns = [
    path('', PostListAPIView.as_view()),
    path('create/', PosCreateAPIView.as_view()),
    path('<uuid:pk>/', PostRetrieveUpdateDestroyAPIView.as_view()),
    path('<uuid:id>/comments/', PostCommentListAPIView.as_view()),
]





