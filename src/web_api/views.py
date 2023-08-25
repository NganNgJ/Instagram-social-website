from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from web_api.error_codes import ERROR_CODES
from rest_framework.exceptions import ParseError
from django.contrib.auth.models import User 
from rest_framework import generics,status,serializers
from web_api.enum import (
    Status
)
from .serializers import (
    RegistrationSerializer,
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
        

@api_view(['GET'])
# @permission_classes([AllowAny])
def get_test(request):
    return Response('ACTIVE')

# raise ParseError(ERROR_CODES[400001], 400001)
# Status.ACTIVE.name .value
