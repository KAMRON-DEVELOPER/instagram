from django.db import models
from uuid import uuid4


class BaseModel(models.Model):
    id = models.UUIDField(unique=True, default=uuid4, editable=False, primary_key=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True