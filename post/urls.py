from django.urls import path

from .views import *




urlpatterns = [
    path('', PostListAPIView.as_view()),
]





