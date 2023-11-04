from django.contrib import admin
from django.urls import path, include
from web_api.views import RegistrationAPIview
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings
from web_api import routing

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('web_api.urls')),
    # path('ui/', include('ui.urls')),
    path('auth/register',RegistrationAPIview.as_view(),name='register,'),
    path('auth/login', TokenObtainPairView.as_view(), name= 'login'),
    path('auth/refresh-token',TokenRefreshView.as_view(), name= 'refreshtoken'),
    path('socket.io/', include(routing.websocket_urlpatterns), name='websocket'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)