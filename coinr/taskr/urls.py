from django.urls import path

from .views import CoinTaskViewSet

urlpatterns = [
    path('coin-task/', CoinTaskViewSet.as_view(), name='coin-task')
]