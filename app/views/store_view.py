
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from app.models import Store, Shop
from ..serializer.store_serializer import StoreDetailSerializer, StoreListSerializer


class StoreView(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreListSerializer
    permission_classes = [IsAuthenticated, ]

    @action(methods=["get"], detail=UnicodeTranslateError)
    def detail_store(self, request, pk):
        try:
            obj = Store.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"message": "objects does not exsist"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = StoreDetailSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
