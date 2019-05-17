import json

from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets,mixins
from django.core.cache import cache

from goods.filters import GoodFilter
from goods.models import *
from goods.serializers import *

#官网上有提供
class Home(APIView):
    def get(self, request):

        # 使用redia进行缓存
        conn = get_redis_connection()
        if not conn.hget('goods', 'main_wheels'):
            main_wheels = MainWheel.objects.all()
            value = json.dumps(MainWheelSerializer(main_wheels, many=True).data)
            conn.hset('goods', 'main_wheels', value)
        redis_main_wheels = json.loads(conn.hget('goods', 'main_wheels'))

        if not conn.hget('goods', 'main_navs'):
            main_navs = MainNav.objects.all()
            value = json.dumps(MainWheelSerializer(main_navs, many=True).data)
            conn.hset('goods', 'main_navs', value)
        redis_main_navs = json.loads(conn.hget('goods', 'main_navs'))

        if not conn.hget('goods', 'main_mustbuys'):
            main_mustbuys = MainMustBuy.objects.all()
            value = json.dumps(MainMustBuySerializer(main_mustbuys, many=True).data)
            conn.hset('goods', 'main_mustbuys', value)
        redis_main_mustbuys = json.loads(conn.hget('goods', 'main_mustbuys'))

        if not conn.hget('goods', 'main_shops'):
            main_shops = MainShop.objects.all()
            value = json.dumps(MainShopSerializer(main_shops, many=True).data)
            conn.hset('goods', 'main_shops', value)
        redis_main_shops = json.loads(conn.hget('goods', 'main_shops'))

        if not conn.hget('goods', 'main_shows'):
            main_shows = MainShow.objects.all()
            value = json.dumps(MainShowSerializer(main_shows, many=True).data)
            conn.hset('goods', 'main_shows', value)
        redis_main_shows = json.loads(conn.hget('goods', 'main_shows'))

        res = {
            'main_wheels': redis_main_wheels,
            'main_navs': redis_main_navs,
            'main_mustbuys': redis_main_mustbuys,
            'main_shops': redis_main_shops,
            'main_shows': redis_main_shows,
        }

        return Response(res)


@api_view(['GET'])
def home(request):
    main_wheels = MainWheel.objects.all()
    main_navs = MainNav.objects.all()
    main_mustbuys = MainMustBuy.objects.all()
    main_shops = MainShop.objects.all()
    main_shows = MainShow.objects.all()
    res = {
        'main_wheels': MainWheelSerializer(main_wheels, many=True).data,
        'main_navs': MainNavSerializer(main_navs, many=True).data,
        'main_mustbuys': MainMustBuySerializer(main_mustbuys, many=True).data,
        'main_shops': MainShopSerializer(main_shops, many=True).data,
        'main_shows': MainShowSerializer(main_shows, many=True).data,
    }

    return Response(res)

class FoodTypeView(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = FoodType.objects.all()
    serializer_class = FoodTypeSerializer



class MarketView(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    filter_class = GoodFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        #子分类 切割解析
        #  全部分类:0#饮用水:103550#茶饮/咖啡:103554#功能饮料:103553#酒类:103555#果汁饮料:103551#碳酸饮料:103552#整箱购:104503#植物蛋白:104489#进口饮料:103556
        typeid = self.request.query_params.get('typeid')
        foodtype = FoodType.objects.filter(typeid=typeid).first()
        foodtype_childname_list = [{'child_name':childnames.split(':')[0],
                                    'child_value':childnames.split(':')[1]}
                                   for childnames in foodtype.childtypenames.split('#')]

        order_rule_list = [
            {'order_name': '综合排序', 'order_value': 0},
            {'order_name': '价格升序', 'order_value': 1},
            {'order_name': '价格降序', 'order_value': 2},
            {'order_name': '销量升序', 'order_value': 3},
            {'order_name': '销量降序', 'order_value': 4},
        ]

        res = {
            'goods_list': serializer.data,
            'order_rule_list': order_rule_list,
            'foodtype_childname_list': foodtype_childname_list,
        }

        return Response(res)