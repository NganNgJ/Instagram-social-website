from rest_framework import routers
from django.urls import path, include
from web_api.views import (
    get_test
)


router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('test', get_test)
  
]