from rest_framework import routers
from django.urls import path, include
from .views import (
    PostCreateViewset,UploadFileViewset
)



router = routers.DefaultRouter()
router.register(r'posts',PostCreateViewset)
router.register(r'upload-file',UploadFileViewset)


urlpatterns = [
    path('', include(router.urls)),

]
