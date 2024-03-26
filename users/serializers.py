from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from shared.utiitys import check_email_or_phone_number, send_email, send_phone_code
from .models import User, UserConfirmation, AUTH_STATUS, AUTH_TYPE, USER_GENDER, USER_ROLES
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password
import re




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
    print('first_name: ', first_name)
    
    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
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
    
    def validate_username(self, data):
        username = data.get('username')
        if len(username) < 3 or len(username) > 15 or username.isnumeric():
            raise ValidationError(
                {
                    'request status' : 'bad 404',
                    'message' : 'your username is not valid!'
                }
            )
    
    def validate_names(self, first_name, last_name):
        for data in [first_name, last_name]:
            if len(data) < 3 or len(data) > 15 or data.isnumeric():
                raise ValidationError(
                    {
                        'request status' : 'bad 404',
                        'message' : 'your first name or last name is not valid!'
                    }
                )
                break
        
    


class ChangeUserInfo(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        super(ChangeUserData, self).__init__(*args, **kwargs)
        self.fields['confirm_password'] = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('username', 'password')
        
        


