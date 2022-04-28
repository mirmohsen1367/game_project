
from rest_framework import serializers
from app.models import Store, Shop


class StoreListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = ("id", "name", "link")


class ShopSerializer(serializers.ModelSerializer):

    type = serializers.CharField(source='get_type_display')
    pay_type = serializers.CharField(source='get_pay_type_display')

    class Meta:
        model = Shop
        fields = ("value", "pay_value", "type", "pay_type", "image_link")


class StoreDetailSerializer(serializers.ModelSerializer):
    shopes = ShopSerializer(many=True)

    class Meta:
        model = Store
        fields = ("shopes",)
