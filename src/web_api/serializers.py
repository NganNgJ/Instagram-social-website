from rest_framework import serializers
from django.contrib.auth.models import User 
from web_api.models import (
    Post,UploadFile,UserTag,PostFile
)

class RegistrationSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(max_length=50, min_length=6)
    username = serializers.CharField(max_length=50, min_length=6)
    password = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username' , 'password')
    
    def validate(self, args):
        email = args.get('email', None)
        username = args.get('username', None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email':('Email already exists')})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username':('Username already exists')})
        return super().validate(args)        

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id', 'first_name' , 'last_name' , 'username', 'is_active')
        
class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = '__all__'

class PostFileSerializer(serializers.ModelSerializer):
    file = UploadFileSerializer(read_only=True)

    class Meta:
        model = PostFile
        fields = '__all__'

class UserTagSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model= UserTag
        fields = '__all__'

class PostCreateSerializer(serializers.ModelSerializer):
    file_ids = serializers.ListField(write_only=False, required=False)
    tagged_user_ids = serializers.ListField(write_only=False, required=False)
    user_id = serializers.CharField(required=True, allow_null=False, write_only=True)
    user = UserSerializer(read_only=True)
    medias = serializers.SerializerMethodField(read_only=True)
    tagged_users = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post 
        fields = '__all__'

    def get_medias(self, obj):
        post_files = obj.post_files.all()
        medias = [UploadFileSerializer(post_file.file).data for post_file in post_files]
        return medias

    def get_tagged_users(self,obj):
        tagged_users_info = obj.user_tags.all()
        tagged_users = [UserSerializer(tagged_user.user).data for tagged_user in tagged_users_info]
        return tagged_users

    def create(self, validated_data):
        file_ids = validated_data.get('file_ids', [])
        tagged_users = validated_data.get('tagged_user_ids',[])
        validated_data.pop('file_ids')
        validated_data.pop('tagged_user_ids')
        post = Post.objects.create(**validated_data)

        for file_id in file_ids:
            try:
                file = UploadFile.objects.get(id=file_id)
                PostFile.objects.create(post=post, file=file)
            except UploadFile.DoesNotExist:
                pass
        for tagged_user_id in tagged_users:
            try:
                user= User.objects.get(id=tagged_user_id)  
                UserTag.objects.create(post=post, user=user)
            except User.DoesNotExist:
                pass 
        return post
    

    

    