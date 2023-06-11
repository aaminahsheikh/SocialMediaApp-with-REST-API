from django.contrib import admin
from . models import CreatePost, User

# Register your models here.
admin.site.register(User)
admin.site.register(CreatePost)
