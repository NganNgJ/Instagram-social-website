from rest_framework.response import Response
from django.http import JsonResponse 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from web_api.error_codes import ERROR_CODES
from rest_framework.exceptions import ParseError
from django.contrib.auth.models import User 
from rest_framework import generics,status,serializers,viewsets
from web_api.enum import (
    Status
)
from .models import (
    Post,UploadFile,Reaction,Comment,CommentReply
)
from .serializers import (
    RegistrationSerializer,
    UploadFileSerializer,
    PostSerializer,
    ReactionSerializer,
    CommentSerializer,
    CommentReplySerializer
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
    queryset = Post.objects.all().order_by('-id')


class ReactionViewset(viewsets.ModelViewSet):
    serializer_class = ReactionSerializer
    queryset = Reaction.objects.all().order_by('-id')


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all().order_by('-id')

    def list(self, request):
        comment_list = self.queryset.filter(is_hidden=False).order_by('-id')
        serializer = CommentSerializer(comment_list, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        comment_id = self.kwargs['pk']
        comment = Comment.objects.get(id=comment_id)
        if comment.is_hidden is True :
            return JsonResponse({'message': 'This comment is already deleted'})
        comment.is_hidden = True
        comment.save()
        return JsonResponse({'message': 'You deleted successfully'})
    
class CommentReplyViewset(viewsets.ModelViewSet):
    serializer_class = CommentReplySerializer
    queryset = CommentReply.objects.all().order_by('-id')

    def list(self, request):
        comment_reply_list = self.queryset.filter(is_hidden=False).order_by('-id')
        serializer = CommentReplySerializer(comment_reply_list, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        comment_reply_id = self.kwargs['pk']
        comment_reply = CommentReply.objects.get(id=comment_reply_id)
        if comment_reply.is_hidden is True :
            return JsonResponse({'message': 'This comment is already deleted'})
        comment_reply.is_hidden = True
        comment_reply.save()
        return JsonResponse({'message': 'You deleted successfully'})