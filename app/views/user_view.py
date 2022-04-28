
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from app.models import User
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from app.models import UserProfile, Device
from app.serializer.user_serializer import UserProfileCreateSerializer, UserSerializer, UserProfileUpdateSerializer, \
    UserProfileInfoSerializer, UserLeaderBoardSerializer
from app.models import GroheUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth
import string
import random
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from django.db.models import Count


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        '''
            this method for add user to save serializer when called and
            pass serializer argumans
        '''

        serializer.save(user=self.request.user.pk)

    test_param = openapi.Parameter('device_id', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_STRING)
    user_response = openapi.Response('response description', UserSerializer)

    @swagger_auto_schema(method='get', manual_parameters=[test_param], responses={200: user_response})
    @action(methods=["get"], detail=False, permission_classes=[AllowAny, ])
    def registrition_device(self, request):
        '''

        :param request: device id sended
            createuser with username and password randpmly
        :return: username
        '''
        if not 'device_id' in request.GET:
            return Response({"message": "pleae enter device_id"}, status=status.HTTP_200_OK)
        letters = string.ascii_lowercase + string.ascii_uppercase
        result_str = ''.join(random.choice(letters) for _ in range(8))
        user = User.objects.create_user(username=result_str, password=result_str)
        _ = Device.objects.create(device_id=request.GET.get("device_id"), user_id=user.id)
        groups_users = GroheUser.objects.annotate(counts_users=Count("user"))
        groups_users.filter(counts_users__lt=100).order_by("-counts_users")
        if groups_users:
            gr = groups_users[0]
            gr.users.add(user)
            return Response({"message": user.username}, status=status.HTTP_200_OK)
        gr = GroheUser.objects.create()
        gr.users.add(user)
        return Response({"message": user.username}, status=status.HTTP_200_OK)

    @swagger_auto_schema(methods=['post'], operation_description="login", request_body=UserSerializer)
    @action(methods=["post"], detail=False, permission_classes=[AllowAny])
    def log_in(self, request):
        '''
          posted username and password
          if username and password authenticate
          :return jwt
        '''
        user = auth.authenticate(request, username=request.data["username"], password=request.data["password"])
        if user is not None:
            refresh = RefreshToken.for_user(user)
            raw_token = str(refresh.access_token)
            return Response({
                "token": str(raw_token)
            })
        return Response({"message": "user was not found"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(methods=['post'], operation_description="post_profile_user", request_body=UserProfileCreateSerializer)
    @action(methods=["post", "get"], detail=False, permission_classes=[IsAuthenticated,], parser_classes=(MultiPartParser,))
    def user_profile(self, request):
        '''
            create and get userprofile view
        '''
        if request.method == "POST":
            serializer = UserProfileCreateSerializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response({"message": "created", "id": serializer.instance.id}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == "GET":
            serializer = UserProfileInfoSerializer(request.user)
            return Response(serializer.data)

            # try:
            #     user_profile = UserProfile.objects.get(user_id=request.user.id)
            # except ObjectDoesNotExist:
            #     return Response({"message": "you not have profile"}, status=status.HTTP_400_BAD_REQUEST)
            # serializer = UserProfileInfoSerializer(user_profile)
            # return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=False, permission_classes=[IsAuthenticated,])
    def update_user_profile(self, request):
        '''
            updated profile user nickname and password
        '''
        try:
            profile = UserProfile.objects.get(user_id=request.user.id)
        except ObjectDoesNotExist:
            return Response({"message": "your not have a profile"}, status=status.HTTP_200_OK)

        data = {}
        # updated request data becuase rest is nested
        for x in request.data:
            if x == "password":
                data.update({"user": {"password": request.data["password"]}})
            if x == "nickname":
                data.update({"nickname": request.data["nickname"]})
        serializer = UserProfileUpdateSerializer(profile, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["post"], detail=False, permission_classes=[IsAuthenticated,])
    def update_profile_image(self, request):
        try:
            profile = UserProfile.objects.get(user_id=request.user.id)
        except ObjectDoesNotExist:
            return Response({"message": "your not have a profile"}, status=status.HTTP_200_OK)
        serializer = UserProfileCreateSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"], detail=False, permission_classes=[IsAuthenticated,])
    def user_leader_board(self, request):
        group = request.user.user_group
        list_of_users = group.users.all().order_by("-point")
        serializer = UserLeaderBoardSerializer(list_of_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

