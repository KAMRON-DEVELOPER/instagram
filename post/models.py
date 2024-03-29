from django.db import models
from users.models import User
from django.contrib.auth import get_user_model
from shared.models import BaseModel
from django.core.validators import FileExtensionValidator, MaxLengthValidator


class Post(BaseModel):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts') # User.posts.all()
    body = models.TextField()
    post_image = models.ImageField(upload_to='post_images/', default='post_images/post_default.jpg', 
                                   validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])])
    
    class Meta:
        db_table = "posts" # default post_post 1-app name, 2-model name
        
    def __str__(self):
        return self.title
    

