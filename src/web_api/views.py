from rest_framework.response import Response
from django.http import JsonResponse 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from web_api.error_codes import ERROR_CODES
from rest_framework.exceptions import ParseError
from django.core.paginator import Paginator
from django.contrib.auth.models import User 
from rest_framework import generics,status,serializers,viewsets
from web_api.enum import (
    Status
)
from .models import (
    Post,UploadFile,Reaction,Comment,Friend,Profile
)
from .serializers import (
    RegistrationSerializer,
    UploadFileSerializer,
    PostSerializer,
    ReactionSerializer,
    CommentSerializer,
    FriendSerializer,
    UserProfileSerializer
)


class RegistrationAPIview(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class= RegistrationSerializer

    def post(self,request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response({'detail': serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        

class UploadFileViewset(viewsets.ModelViewSet):
    serializer_class = UploadFileSerializer
    queryset = UploadFile.objects.all()

    def perform_create(self, serializer):
        file = self.request.data.get('file')
        file_type = file.name.split('.')[-1]

        serializer.save(file_type = file_type)


class PostViewset(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(is_hidden=False).order_by('-id')

    def destroy(self, request, *args, **kwargs):
        post_id = self.kwargs['pk']
        post = Post.objects.filter(id=post_id).first()
        if post is None:
            return JsonResponse({'message': 'Post not found'})
        if post.is_hidden is True:
            return JsonResponse({'message': 'This post is already deleted'})
        post.is_hidden = True
        post.save()
        return JsonResponse({'message': 'You deleted successfully'})


class ReactionViewset(viewsets.ModelViewSet):
    serializer_class = ReactionSerializer
    queryset = Reaction.objects.all().order_by('-id')


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all().order_by('-id')

    def list(self, request):
        comment_list = self.queryset.filter(is_hidden=False, parent_comment__isnull=True).order_by('-id')
        serializer = CommentSerializer(comment_list, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        comment_id = self.kwargs['pk']
        comment = Comment.objects.filter(id=comment_id).first()
        if comment is None:
            return JsonResponse({'message': 'Comment not found'})
        if comment.is_hidden is True :
            return JsonResponse({'message': 'This comment is already deleted'})
        comment.is_hidden = True
        comment.save()
        return JsonResponse({'message': 'You deleted successfully'})
    
class FriendViewset(viewsets.ModelViewSet):
    serializer_class = FriendSerializer
    queryset=User.objects.all().order_by('-id')


@api_view(['POST'])
def block_user(request):
    user_id = request.data.get('user_id')
    block_user_id = request.data.get('block_user_id')

    user = User.objects.filter(id=user_id).first()
    block_user = User.objects.filter(id=block_user_id).first()

    if user is None:
        raise serializers.ValidationError({'users':('This user is not found')})
    if block_user is None:
        raise serializers.ValidationError({'users':('This block user is not found')})
    
    friend = Friend.objects.filter(user_id=user_id, friend_id=block_user_id).first()

    if friend is None:
        friend = Friend.objects.create(user_id = user_id, friend_id = block_user_id, is_followed = False, is_blocked = True)
    else:
        friend.is_blocked = not friend.is_blocked
        friend.save()

    if friend.is_blocked:
        return JsonResponse({'message': '{0} has been blocked by user {1}'.format(block_user.username, user.username)})
    else:
        return JsonResponse({'message': '{0} has been unblocked by user {1}'.format(block_user.username, user.username)})
    
class UserProfileViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    
    