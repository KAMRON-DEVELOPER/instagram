from django.shortcuts import render
from .models import AUTH_STATUS, User, UserConfirmation
from .serializers import SignUpSerializer
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from django.utils import timezone
from rest_framework.validators import ValidationError
from rest_framework.response import Response


class CreateUserView(CreateAPIView):
    model = User
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)


class VerifyApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        code = request.data.get('code')
        
        self.check_verify(user, code)
        return Response(
            data={
                'request status': 'Well',
                'message': user.AUTH_STATUS,
                'access': user.token()['access'],
                'refresh': user.token()['refresh']
            }
        )
        
    @staticmethod
    def check_verify(user, code):
        iscode_exist = user.verify_code.filter(expiration_time__gte=timezone.now(), code=code, is_confirmed=False)
        exp_time = user.verify_code.all() # expiration_time
        print(exp_time)
        if not iscode_exist.exists():
            data = {
                'request status': 'Yomon',
                'message': 'you verificaton code already expired.'
            }
            raise ValidationError(data)
        else:
            iscode_exist.update(is_confirmed=True)
        if user.auth_status == AUTH_STATUS.new:
            user.auth_status = AUTH_STATUS.verified
            user.save()
        return True
        