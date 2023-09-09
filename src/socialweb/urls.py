"""socialweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from web_api.views import RegistrationAPIview
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('web_api.urls')),
    path('auth/register',RegistrationAPIview.as_view(),name='register,'),
    path('auth/login', TokenObtainPairView.as_view(), name= 'login'),
    path('auth/refresh-token',TokenRefreshView.as_view(), name= 'refreshtoken'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)