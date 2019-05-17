
from rest_framework import viewsets,mixins
# Create your views here.
from rest_framework.decorators import list_route
from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from carts.models import Cart
from carts.serializers import CartSerializer
from user.models import AXFUser
from utils.UserAythebtication import UserAuth


class CartView(viewsets.GenericViewSet,
                mixins.ListModelMixin,
                mixins.UpdateModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = (UserAuth,)


    def list(self,request, *args, **kwargs):
        # {code:200, msg:'', data: {carts:'', total_price:''}}
        queryset = self.get_queryset()
        # 过滤出当前登录系统用户的购物车信息
        queryset = queryset.filter(c_user=request.user)
        serializer = self.get_serializer(self.get_queryset(), many=True)

        # 计算总价
        queryset = queryset.filter(c_is_select=1).all()
        total_price = 0
        for cart in queryset:
            total_price += cart.c_goods_num * cart.c_goods.price

        res = {
            'carts': serializer.data,
            'total_price': total_price,
        }
        return Response(res)


    @list_route(methods=['POST'])
    def add_cart(self, request, *args, **kwargs):
        # 思路： 登录和没登录情况
        # 1、登录信息的判断，cache使用
        goodsid = request.data.get('goodsid')
        # 2、如果当前登录系统用户已添加同一商品，则商品数量加一
        cart = Cart.objects.filter(c_user=request.user,
                                c_goods_id=goodsid).first()
        if not cart:
            # 购物车种没有该账号添加的对应商品信息
            Cart.objects.create(c_user=request.user,
                                c_goods_id=goodsid)
        else:
            # 购物车中有该账号添加的商品信息
            cart.c_goods_num += 1
            cart.save()
        res = {
            'code': 200,
            'msg': '添加成功'
        }
        return Response(res)

    @list_route(methods=['POST'])
    def sub_cart(self, request, *args, **kwargs):
        goodsid = request.data.get('goodsid')
        cart = Cart.objects.filter(c_user=request.user,
                                   c_goods_id=goodsid).first()
        if cart:
            if cart.c_goods_num > 1:
                cart.c_goods_num -= 1
                cart.save()
            else:
                cart.delete()
        res = {'code': 200, 'msg': '删除成功'}
        return Response(res)


    # @list_route(methods=['POST'])
    # def add_cart(self, request, *args, **kwargs):
    #     # 思路： 登录和没登录情况
    #     # 1、登录信息的判断，cache使用
    #     token = request.data.get('token')
    #     goodsid = request.data.get('goodsid')
    #     user_id = cache.get(token)
    #     res = {}
    #     if user_id:
    #         # 2、如果当前登录系统用户已添加同一商品，则商品数量加一
    #         cart = Cart.objects.filter(c_user_id=user_id,
    #                             c_goods_id=goodsid).first()
    #         if not cart:
    #             # 购物车种没有该账号添加的对应商品信息
    #             Cart.objects.create(c_user_id=user_id,
    #                                 c_goods_id=goodsid)
    #         else:
    #             # 购物车中有该账号添加的商品信息
    #             cart.c_goods_num += 1
    #             cart.save()
    #             res = {
    #                 'code': 200,
    #                 'msg': '添加成功'
    #             }
    #
    #     # 3、如果当前登录系统用户没有添加商品，则创建购物车中的信息
    #     else:
    #         # 4、没有登录，直接返回状态码
    #         res = {
    #             'code': 1007,
    #             'msg': '用户没有登录，清闲登录，再操作'
    #         }
    #     return Response(res)


    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        instance.c_is_select = not instance.c_is_select
        instance.save()
        res = {
            'code': 200,
            'msg': '修改成功'
        }
        return Response(res)

    @list_route(methods=['PATCH'])
    def change_select(self, request, *args, **kwargs):
        # 修改当前登录用户的购物车中的商品的所有选择状态
        user = request.user
        Cart.objects.filter(c_user=user).update(c_is_select=1)
        res = {
            'code': 200,
            'msg': '修改成功'
        }
        return Response(res)