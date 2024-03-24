from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from shared.utiitys import check_email_or_phone_number
from .models import User, UserConfirmation, AUTH_STATUS, AUTH_TYPE, USER_GENDER, USER_ROLES




class SignUpSerialzer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    def __init__(self, *args, **kwargs):
        super(SignUpSerialzer, self).__init__(*args, **kwargs)
        self.fields['email_phone_number'] = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'date_of_birth', 'user_roles', 'user_gender', 'auth_type', 'auth_status']
        extra_kwargs = {
            'auth_type' : {'read_only' : True, 'required' : False}
        }
        
    def validate(self, attrs):
        super(SignUpSerialzer, self).validate(attrs)
        data = self.auth_validate(attrs)
        return data
    
    @staticmethod
    def auth_validate(data):
        user_input = str(data.get('email_phone_number'))
        input_type = check_email_or_phone_number(user_input)
        print("user_input: ", user_input)
        print("input_type: ", input_type)
        
    
        