from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
import uuid

class Profile(BaseModel):  # Inherit from BaseModel if it has reusable fields
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True,default='profile_images/default.png')

    def __str__(self):
        return self.user.username

    def full_name(self):
        return f"{self.user.username} {self.user_type}"
