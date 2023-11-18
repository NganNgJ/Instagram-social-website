from django.contrib import admin
from django.urls import path, include
from web_api.views import RegistrationAPIview
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings
from web_api import routing
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions



schema_view = get_schema_view(
    openapi.Info(
        title="Episyche Technologies",
        default_version='v1',),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('web_api.urls')),
    path('auth/register',RegistrationAPIview.as_view(),name='register,'),
    path('auth/login', TokenObtainPairView.as_view(), name= 'login'),
    path('auth/refresh-token',TokenRefreshView.as_view(), name= 'refreshtoken'),
    path('socket.io/', include(routing.websocket_urlpatterns), name='websocket'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)