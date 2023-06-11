from rest_framework import serializers

from home.models import CreatePost, User

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatePost
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        