from rest_framework import routers
from django.urls import path, include
from .views import (
    PostViewset,
    UploadFileViewset,
    ReactionViewset
)



router = routers.DefaultRouter()
router.register(r'posts',PostViewset)
router.register(r'upload-file',UploadFileViewset)
router.register(r'react-post',ReactionViewset)


urlpatterns = [
    path('', include(router.urls)),

]
