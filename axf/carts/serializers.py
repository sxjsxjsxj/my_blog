from rest_framework import serializers

from carts.models import Cart

from goods.serializers import GoodsSerializer

class CartSerializer(serializers.ModelSerializer):

    c_goods = GoodsSerializer()

    class Meta:
        model = Cart
        fields = '__all__'



class AddCartSerializer(serializers.Serializer):
    token=serializers.CharField()
    goodsid=serializers.CharField()

