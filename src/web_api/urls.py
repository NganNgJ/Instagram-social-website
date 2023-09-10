from rest_framework import routers
from django.urls import path, include
from .views import (
    PostViewset,UploadFileViewset
)



router = routers.DefaultRouter()
router.register(r'posts',PostViewset)
router.register(r'upload-file',UploadFileViewset)


urlpatterns = [
    path('', include(router.urls)),

]
