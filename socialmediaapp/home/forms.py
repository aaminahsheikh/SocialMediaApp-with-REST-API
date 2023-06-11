from django.forms import ModelForm
from . models import CreatePost, User
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

    
class CreatePostForm(ModelForm):
    class Meta:
        model = CreatePost
        fields = ['body']

        
