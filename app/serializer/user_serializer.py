
from rest_framework import serializers
from app.models import UserProfile, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class UserProfileCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = "__all__"


class userProfileInfoSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = "__all__"