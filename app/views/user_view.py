from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from app.models import User
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from app.models import UserProfile
from rest_framework_simplejwt.authentication import JWTAuthentication
from app.serializer.user_serializer import UserProfileCreateSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]

    action(methods=["post"], detail=False, permission_class=[IsAuthenticated, AllowAny])
    def log_in(self, request):
        user = auth.authenticate(request, username=request.data["username"], password=request.data["password"])
        if user is not None:
            refresh = RefreshToken.for_user(user)
            raw_token = str(refresh.access_token)
            return Response({
                "token": str(raw_token)
            })
        return Response({"message": "user was not found"}, status=status.HTTP_400_BAD_REQUEST)

    action(methods=["post", "get", "patch"], detail=False, permission_class=[IsAuthenticated,])
    def register_info_user(self, request):
        if request.method == "POST":
            serializer = UserProfileCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == "GET":
            user_profile = UserProfile.objects.get(user_id=request.user.id)



