from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    not_admin = models.BooleanField(default=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class CreatePost(models.Model):
    post_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post_likes = models.ManyToManyField(User, related_name="create_post_like", blank=True)

    # Keep track of total likes
    def num_of_likes(self):
        return self.post_likes.count()
    
    class Meta:
        ordering = ['-created_at', '-updated_at']

    def __str__(self):
        return self.body[:50]
    
    