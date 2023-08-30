from rest_framework import routers
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)