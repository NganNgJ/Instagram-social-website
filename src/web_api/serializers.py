from rest_framework import serializers
from django.contrib.auth.models import User 
from web_api.models import (
    Post,Image,Video,UserTag
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
        
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('video',)

class UsertagSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTag
        fields = ('user',)

class PostCreateSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, required=False)
    videos = VideoSerializer(many=True, required=False)
    users = UsertagSerializer(many=True, required=False)
    
    class Meta:
        model = Post 
        fields = ('description', 'user_id', 'tagged_user', 'is_hidden', 'images', 'videos')

    def create(self,validated_data):
        images_data = validated_data.pop('images',[])
        videos_data = validated_data.pop('videos',[])
        users_tag_data = validated_data.pop('users', [])
        post = Post.objects.create(**validated_data)
        
        for image in images_data:
            Image.objects.create(post=post, **image)

        for video in videos_data:
            Video.objects.create(post=post, **video)
        
        for user in users_tag_data:
            UserTag.objects.create(post=post, **user)

        return post