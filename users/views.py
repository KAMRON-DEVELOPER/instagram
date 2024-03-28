from django.shortcuts import render
from django.views import View

from shared.utiitys import send_email
from .models import AUTH_STATUS, AUTH_TYPE, User, UserConfirmation
from .serializers import SignUpSerializer, ChangeUserData, ChangeUserPhotoSerializer, LoginSerializer, LoginRefreshSerializer
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from datetime import datetime, timedelta
from rest_framework.validators import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView




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
                'message': user.auth_status,
                'access': user.token()['access'],
                'refresh': user.token()['refresh_token']
            })
        
    @staticmethod
    def check_verify(user, code):
        iscode_exist = user.verify_code.filter(expiration_time__gte=datetime.now(), code=code, is_confirmed=False)
        exp_time = user.verify_code.all()
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



class GetNewVerifyApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        user = self.request.user
        self.check_verify_user(user)
        if user.auth_type == AUTH_TYPE.email:
            code = user.create_verify_code(AUTH_TYPE.email)
            send_email(user.email, code)
        elif user.auth_type == AUTH_TYPE.phone_number:
            code = user.create_verify_code(AUTH_TYPE.phone_number)
            send_email(user.phone_number, code)
        else:
            data={
                    'request status: ' : 'Unknown!',
                    'message: ' : 'Somthing went wrong in creating code for you?!'
            }
            raise ValidationError(data)
        
        return Response(
            {
                'request status': 'Good!!!!!',
                'message': 'your code sent again!'
            })

    @staticmethod
    def check_verify_user(user):
        iscode_exist = user.verify_code.filter(expiration_time__gte=datetime.now(), is_confirmed=False)
        if iscode_exist.exists():
            data = {
                "message": "Kodingiz hali ishlatish uchun yaroqli. Biroz kutib turing"
            }
            raise ValidationError(data)

            
            

class ChangeUserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    print("ChangeUser view ishladi!")
    
    def post(self, request, *args, **kwargs):
        first_name = self.request
        print(first_name)
        return Response({"first_m=name" : first_name})
            
            

class ChangeUserInformationView(UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangeUserData
    http_method_names = ['patch', 'put']     
            
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        super(ChangeUserInformationView, self).update(request, *args, **kwargs)        

        return Response(
            {
                'request status' : 'ok 200',
                'message' : 'user information has been updated!',
                'auth_status' : self.request.user.auth_status
            }
        )
        
    def partial_update(self, request, *args, **kwargs):
        super(ChangeUserInformationView, self).partial_update(request, *args, **kwargs)        

        return Response(
            {
                'request status' : 'ok 200',
                'message' : 'user information has been updated!',
                'auth_status' : self.request.user.auth_status
            }
        )



class ChangeUserPhotoView(UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def put(self, request, *args, **kwargs):
        serializer = ChangeUserPhotoSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            serializer.update(user, serializer.validated_data)
            return Response(
                {
                    'request status' : 'ok 200',
                    'message' : 'your photo has been updated!'
                }
            )
        return Response(
            {
                    'request status' : 'bad 400',
                    'message' : 'issue occured while updating your photo!',
                    'errors' : serializer.errors
                }
        )



class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer







