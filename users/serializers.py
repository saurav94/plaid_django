from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from django.contrib.auth import authenticate

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # user = User(
        #     email=validated_data['email'],
        #     username=validated_data['username']
        # )
        # user.set_password(validated_data['password'])
        # user.save()
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(max_length=100)
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']
    
    # def validate(self, data):
    #     """
    #     Check if user exists.
    #     """
    #     username = data['username']
    #     password = data['password']
    #     user = authenticate(username=username, password=password)

    #     if user is None:
    #         raise serializers.ValidationError("Invalid credentials")

    #     return data