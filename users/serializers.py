from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from shared.utiitys import check_email_or_phone_number
from .models import User, UserConfirmation, AUTH_STATUS, AUTH_TYPE, USER_GENDER, USER_ROLES




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
    
