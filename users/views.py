from django.shortcuts import render
from .models import User, UserConfirmation
from .serializers import SignUpSerializer
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import permission_classes


class CreateUserView(CreateAPIView):
    model = User
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

