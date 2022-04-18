
from rest_framework import serializers
from app.models import UserProfile, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "password", "email")

        extra_kwargs = {'password': {'write_only': True}}


class UserProfileCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ("nickname", "avatar")


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "email")


class userProfileInfoSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ("id", "nickname", "image_link", "user")

    def update(self, instance, validated_data):
        user = validated_data.get("user", None)
        if user:
            instance.user.username = user.get("username", instance.user.username)
            if "password" in user:
                instance.user.set_password(user.get("password"))
            instance.user.save()
        instance.nickname = validated_data.get("nickname", self.instance.nickname)
        instance.save()
        return instance
