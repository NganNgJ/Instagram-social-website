from rest_framework import routers
from django.urls import path, include
from .views import (
    PostViewset,
    UploadFileViewset,
    ReactionViewset,
    CommentViewset,
    FriendViewset,
    block_user,
    UserProfileViewset
)



router = routers.DefaultRouter()
router.register(r'posts',PostViewset)
router.register(r'upload-file',UploadFileViewset)
router.register(r'react-post',ReactionViewset)
router.register(r'comments',CommentViewset)
router.register(r'friends',FriendViewset)
router.register(r'user-profile',UserProfileViewset)


urlpatterns = [
    path('', include(router.urls)),
    path('block-user/',block_user)
]
