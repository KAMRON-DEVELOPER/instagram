from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from shared.utiitys import check_email_or_phone_number, send_email, send_phone_code, check_login_type
from .models import User, UserConfirmation, AUTH_STATUS, AUTH_TYPE, USER_GENDER, USER_ROLES
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password
import re
from django.core.validators import FileExtensionValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate




class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    def __init__(self, *args, **kwargs):
        super(SignUpSerializer, self).__init__(*args, **kwargs)
        self.fields['email_phone_number'] = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ('id', 'auth_type', 'auth_status')
        extra_kwargs = {
            'auth_type': {'read_only': True, 'required': False},
            'auth_status': {'read_only': True, 'required': False}
        }
        
    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)
        print(user)
        if user.auth_type == AUTH_TYPE.email:
            code = user.create_verify_code(AUTH_TYPE.email)
            print('code: ', code)
            send_email(user.email, code)
        elif user.auth_type == AUTH_TYPE.phone_number:
            code = user.create_verify_code(AUTH_TYPE.phone_number)
            print('code: ', code)
            send_email(user.phone_number, code)
        user.save()
        return user
        
    def validate(self, data):
        super(SignUpSerializer, self).validate(data)
        data = self.auth_validate(data)
        return data
    
    @staticmethod
    def auth_validate(data):
        print(data)
        user_input = str(data.get('email_phone_number'))
        input_type = check_email_or_phone_number(user_input)
        print("user_input: ", user_input)
        print("input_type: ", input_type)
        
        if input_type == "email":
            data = {
                "email": user_input,
                "auth_type": AUTH_TYPE.email
            }
        elif input_type == "phone_number":
            data = {
                "phone_number": user_input,
                "auth_type": AUTH_TYPE.phone_number
            }
        else:
            data = {
                "request status": "Terrible!",
                'message': "You must send email or phone number"
            }
            raise ValidationError(data)

        return data
    
    
    def validate_email_phone_number(self, value):
        if value and User.objects.filter(email=value):
            data = {
                'request status' : 'Terrible!',
                'message' : 'this email already exist!'
            }
            raise ValidationError(data)
        elif value and User.objects.filter(phone_number=value):
            data = {
                'request status' : 'Terrible!',
                'message' : 'this phone number already exist!'
            }
            raise ValidationError(data)
        return value
    
    
    def to_representation(self, instance):
        data = super(SignUpSerializer, self).to_representation(instance)
        data.update(instance.token())
        
        return data




class ChangeUserData(serializers.Serializer):
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    
    def validate(self, data):
        password = data.get('password', None)
        confirm_password = data.get('confirm_password', None)
        
        if password != confirm_password:
            raise ValidationError(
                {
                    'request status' : 'bad 404',
                    'message' : 'your password and confirm password must be the same!'
                }
            )
        if password:
            validate_password(password=password)
            validate_password(password=confirm_password)
        return data
    
    def validate_username(self, username):
        if len(username) < 3 or len(username) > 15 or bool(re.search(r'\d', username)):
            raise ValidationError(
                {
                    'request status' : 'bad 404',
                    'message' : 'your username is not valid!'
                }
            )
        return username
    
    def validate_first_name(self, first_name):
        if len(first_name) < 3 or len(first_name) > 15 or bool(re.search(r'\d', first_name)):
            raise ValidationError(
                {
                    'request status' : 'bad 404',   
                    'message' : 'your first name or last name is not valid!'
                }
            )
        return first_name
        
    def validate_last_name(self, last_name):
        if len(last_name) < 3 or len(last_name) > 15 or bool(re.search(r'\d', last_name)):
            raise ValidationError(
                {
                    'request status' : 'bad 404',   
                    'message' : 'your first name or last name is not valid!'
                }
            )
        return last_name
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.password = validated_data.get('password', instance.password)

        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
        if instance.auth_status == AUTH_STATUS.verified:
            instance.auth_status = AUTH_STATUS.done
        instance.save()
        return instance
    

class ChangeUserPhotoSerializer(serializers.Serializer):
    photo = serializers.ImageField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
        
    def update(self, instance, validated_data):
        photo = validated_data.get('photo')
        if photo:
            instance.photo = validated_data.get('photo', instance.photo)
            instance.auth_status = AUTH_STATUS.photo
            instance.save()    
        else:
            raise ValidationError(
                {
                    'request status' : 'bad 404',
                    'message' : 'you have not upload any photo!'
                }
            )
        return instance
        


class LoginSerializer(TokenObtainPairSerializer):
    
    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.fields['user_input'] = serializers.CharField(required=True)
        self.fields['username'] = serializers.CharField(required=False, read_only=True)
        
    def auth_validate(self, data):
        user_input = data.get('user_input')
        
        if check_login_type(user_input) == "username":
            username = user_input
        elif check_login_type(user_input) == "email":
            user = User.objects.get(email__iexact=user_input)
            username = user.username
        elif check_login_type(user_input) == "phone_number":
            user = User.objects.get(phone_number__iexact=user_input)
            username = user.username
        else:
            data = {
                "request status": "Terrible!",
                "message": "Login Interrupted!"
            }
            raise ValidationError(data)
        
        authentication_kwargs = {
            self.username_field : username,
            'password' : data.get('password')
        }

        user = authenticate(authentication_kwargs)

        
        





