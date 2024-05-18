from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSetView
)

router = DefaultRouter()
router.register('category', CategoryViewSetView)


app_name = 'product'

urlpatterns = [
    path('', include(router.urls)),
]
