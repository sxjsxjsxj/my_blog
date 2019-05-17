
from django.urls import path
from rest_framework.routers import SimpleRouter

from goods.views import home, Home, FoodTypeView, MarketView

router = SimpleRouter()
router.register('foodtype',FoodTypeView)
router.register('market', MarketView)

urlpatterns = [
    # function形式，使用api_view装饰器
    # path('home/', home),
    #继承APIView的形式
    path('home/', Home.as_view())
]

urlpatterns += router.urls