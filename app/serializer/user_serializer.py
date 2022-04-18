
from rest_framework import serializers
from app.models import UserProfile, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class UserProfileCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ("nickname", "avatar")


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "email")


class userProfileInfoSerializer(serializers.ModelSerializer):

    user = UserInfoSerializer()

    class Meta:
        model = UserProfile
        fields = ("nickname", "image_link", "user")