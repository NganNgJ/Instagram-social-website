from rest_framework import serializers
from django.contrib.auth.models import User 
from web_api.models import (
    Post,UploadFile,UserTag
)

#tận dụng validate, create, post trong serializer

class RegistrationSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(max_length=50, min_length=6)
    username = serializers.CharField(max_length=50, min_length=6)
    password = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username' , 'password')
    
    def validate(self, args):
        email= args.get('email', None)
        username= args.get('username', None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email':('Email already exists')})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username':('Username already exists')})
        return super().validate(args)        

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        
class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = '__all__'

class PostCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post 
        fields = '__all__'

    def create(self,validated_data):
        post = Post.objects.create(**validated_data)
        return post