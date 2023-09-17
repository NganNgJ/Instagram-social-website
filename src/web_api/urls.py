from rest_framework import routers
from django.urls import path, include
from .views import (
    PostViewset,
    UploadFileViewset,
    ReactionViewset,
    CommentViewset,
    ShareViewset
)



router = routers.DefaultRouter()
router.register(r'posts',PostViewset)
router.register(r'upload-file',UploadFileViewset)
router.register(r'react-post',ReactionViewset)
router.register(r'comments',CommentViewset)
router.register(r'shares',ShareViewset)


urlpatterns = [
    path('', include(router.urls)),

]
