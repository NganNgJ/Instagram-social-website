from rest_framework.response import Response 
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
    Post
)
from .serializers import (
    RegistrationSerializer,
    PostCreateSerializer
)
import uuid


class RegistrationAPIview(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class= RegistrationSerializer

    def post(self,request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response({'detail': serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        

class PostCreateViewset(viewsets.ModelViewSet):
    serializer_class = PostCreateSerializer
    queryset = Post.objects.all().order_by('-id')
