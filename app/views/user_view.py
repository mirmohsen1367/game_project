from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from app.models import User
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from app.models import UserProfile, Device
from app.serializer.user_serializer import UserProfileCreateSerializer, UserSerializer, userProfileInfoSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth
import string
import random


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    @action(methods=["get"], detail=False, permission_classes=[AllowAny, ])
    def registrition_device(self, request):
        if not 'device_id' in request.GET:
            return Response({"message": "pleae enter device_id"}, status=status.HTTP_200_OK)
        letters = string.ascii_lowercase + string.ascii_uppercase
        result_str = ''.join(random.choice(letters) for i in range(8))
        user = User.objects.create_user(username=result_str, password=result_str)
        _ = Device.objects.create(device_id=request.GET.get("device_id"), user_id=user.id)

        return Response({"message": user.username}, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=False, permission_classes=[AllowAny])
    def log_in(self, request):
        user = auth.authenticate(request, username=request.data["username"], password=request.data["password"])
        if user is not None:
            refresh = RefreshToken.for_user(user)
            raw_token = str(refresh.access_token)
            return Response({
                "token": str(raw_token)
            })
        return Response({"message": "user was not found"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["post", "get", "patch"], detail=False, permission_classes=[IsAuthenticated,])
    def user_profile(self, request):
        if request.method == "POST":
            serializer = UserProfileCreateSerializer(data=request.data)
            if serializer.is_valid():
                data = request.data.copy()

                serializer.save(user=request.user)
                serializer.instance.user = request.user
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == "GET":
            user_profile = UserProfile.objects.get(user_id=request.user.id)
            serializer = userProfileInfoSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)


