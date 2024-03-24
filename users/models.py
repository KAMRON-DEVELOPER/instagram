import string
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from random import choice, randint
import uuid
from datetime import datetime, timedelta
from shared.models import BaseModel
from random_username.generate import generate_username
from rest_framework_simplejwt.tokens import RefreshToken
# from django.db import models




class USER_ROLES(models.TextChoices):
    admin = 'admin', 'Admin'
    primitive = 'primitive', 'Primitive'
    manager = 'manager', 'Manager'

class AUTH_TYPE(models.TextChoices):
    email = 'email', 'Email'
    phone_number = 'phone_number', 'Phone_number'

class AUTH_STATUS(models.TextChoices):
    new = 'new', 'New'
    verified = 'verified', 'Verified'
    done = 'done', 'Done'
    photo = 'photo', 'Photo'

class USER_GENDER(models.TextChoices):
    male = 'male', 'Male'
    female = 'female', 'Female'

class User(AbstractUser, BaseModel):
    '''email, phone_number, date_of_birth, user_roles, user_gender, auth_type, auth_status, photo'''
    email = models.EmailField(null=True, unique=True)
    phone_number = models.CharField(max_length=13, unique=True, null=True)
    date_of_birth = models.DateField(editable=True, null=True)
    user_roles = models.CharField(choices=USER_ROLES.choices, default=USER_ROLES.primitive)
    user_gender = models.CharField(choices=USER_GENDER.choices, null=True)
    auth_type = models.CharField(choices=AUTH_TYPE.choices, default=AUTH_TYPE.email)
    auth_status = models.CharField(choices=AUTH_STATUS.choices, default=AUTH_STATUS.new)
    photo = models.ImageField(upload_to='users_photos/', default='users_photos/default.png',
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])

    def __str__(self):
        return self.username
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def create_verify_code(self, verify_type):
        code = "".join(choice(string.digits) for _ in range(4))
        UserConfirmation.objects.create(code=code, verify_type=verify_type, user_id=self.id)
        return code

    def check_email(self):
        if self.email:
            normalized_email = self.email.lower()
            self.email = normalized_email
    
    def check_username(self):
        temp_username = generate_username()[0][:6]
        while User.objects.filter(username=temp_username):
            temp_username += f"_{randint(1000, 9999)}"
        self.username = temp_username

    def check_pass(self):
        self.password = f"{"".join(choice(string.digits) for _ in range(8))}"

    def hash_pass(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)
    
    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access" : str(refresh.access_token),
            "refresh_token" : str(refresh),
        }

    def clean(self):
        self.check_email()
        self.check_username()
        self.check_pass()
        self.hash_pass()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.clean()
        super(User, self).save(*args, **kwargs)




class UserConfirmation(BaseModel):
    '''code, verify_type, user, expiration_time, is_confirmed'''
    code = models.CharField(max_length=4)
    verify_type = models.CharField(choices=AUTH_TYPE.choices, default=AUTH_TYPE.email)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verify_code')
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.__str__())

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.verify_type == AUTH_TYPE.email:
                self.expiration_time = datetime.now() + timedelta(minutes=5)
            else:
                self.expiration_time = datetime.now() + timedelta(minutes=2)
        super(UserConfirmation, self).save(*args, **kwargs)

