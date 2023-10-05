from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User 
from web_api.enum import (
    ReactionType
)
from web_api.models import (
    Post,
    UploadFile,
    UserTag,
    PostFile,
    Reaction,
    Comment,
    Friend,
    Profile
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


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    file_ids = serializers.ListField(write_only=False, required=False)
    tagged_user_ids = serializers.ListField(write_only=False, required=False)
    user_id = serializers.IntegerField(required=True, allow_null=False, write_only=True)
    parent_post_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    medias = serializers.SerializerMethodField(read_only=True)
    tagged_users = serializers.SerializerMethodField(read_only=True)
    

    class Meta:
        model = Post 
        fields = '__all__'

    def validate(self, args):
        user_id = args.get('user_id', None)
        parent_post_id = args.get('parent_post_id', None)
        

        user = User.objects.filter(id=user_id)
        post_share = Post.objects.filter(id=parent_post_id)

        if not user.exists():
            raise serializers.ValidationError({'users':('This user does not exist')})
        if parent_post_id is not None:
            if not post_share.exists():
                raise serializers.ValidationError({'message':('This post does not exist')})
        
        return super().validate(args)  

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
    
    def update(self, instance, validated_data):
        user_id = validated_data['user_id']
        if instance.user_id != user_id:
            raise serializers.ValidationError({'message': 'Error occurs. Can''t edit this post'})

        instance.description = validated_data['description']
        instance.save()
        return instance 

class ReactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    user_id = serializers.IntegerField(required=True, allow_null=False, write_only=True)
    post_id = serializers.IntegerField(required=True, allow_null=False, write_only=True)
    react_type = serializers.CharField(required=True, allow_null=False, write_only=True)
    
    class Meta:
        model = Reaction
        fields = '__all__'
    
    def validate(self, args):
        user_id = args.get('user_id', None)
        post_id = args.get('post_id', None)
        react_type = args.get('react_type', None)

        post = Post.objects.filter(id=post_id)
        
        if not post.exists(): 
            raise serializers.ValidationError({'posts':('This post does not exist')})
        if not User.objects.filter(id=user_id).exists():
            raise serializers.ValidationError({'users':('This user does not exist')})
        if react_type not in [item.value for item in ReactionType]:
            raise serializers.ValidationError({'react_type':('Invalid react_type')})
        
        return super().validate(args) 
    
    def create(self, validated_data):
        user_id = validated_data.get('user_id')
        post_id = validated_data.get('post_id')
        react_type = validated_data.get('react_type')
    
        reaction_filter = Reaction.objects.filter(user_id=user_id, post_id=post_id).first()

        if reaction_filter:
            reaction_filter.react_type = react_type
            reaction_filter.save()
            self.update_post_reacts_count(post_id)
            return reaction_filter
        
        new_reaction = Reaction.objects.create(user_id=user_id, post_id=post_id, react_type=react_type)
        self.update_post_reacts_count(validated_data['post_id']) 
        return new_reaction
    
   
    def update_post_reacts_count(self, post_id):
        love_reacts_count = Reaction.objects.filter(post_id=post_id, react_type=ReactionType.REACTION.value).count()
        post = Post.objects.get(id=post_id)
        post.count_reacts = love_reacts_count
        post.save()
        

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    user_id = serializers.IntegerField(required=True, allow_null=False, write_only=True)
    post_id = serializers.IntegerField(required=True, allow_null=False, write_only=True)
    parent_comment_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    replies = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Comment
        fields = '__all__'
    
    def get_replies(self, obj):
        replies = Comment.objects.filter(parent_comment=obj)
        serializer = ReplyCommentSerializer(replies, many=True)
        return serializer.data

    def validate(self, args):
        user_id = args.get('user_id', None)
        post_id = args.get('post_id', None)
        parent_comment_id = args.get('parent_comment_id', None)
        
        post = Post.objects.filter(id=post_id)
        user = User.objects.filter(id=user_id)
        comment = Comment.objects.filter(id=parent_comment_id, post=post_id)

        
        if not post.exists(): 
            raise serializers.ValidationError({'posts':('This post does not exist')})
        if not user.exists():
            raise serializers.ValidationError({'users':('This user does not exist')})
        if parent_comment_id is not None:
            if not comment.exists():
                raise serializers.ValidationError({'comments':('This comment does not exist')})
        
        return super().validate(args)  
    
    def create(self, validated_data):
        new_comment = Comment.objects.create(**validated_data)
        return new_comment
    
    def update(self, instance, validated_data): 
        user_id = validated_data['user_id']
        post_id = validated_data['post_id']

        if instance.user_id != user_id or instance.post_id != post_id:
            raise serializers.ValidationError({'message': 'Error occurs. Can''t edit this comment'})

        instance.description = validated_data['description']
        instance.save()
        return instance 

class ReplyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('post','parent_comment')

        
class FriendSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    friend = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(required=True, allow_null=False, write_only=True)
    friend_id = serializers.IntegerField(required=True, allow_null=False, write_only=True)

    class Meta:
        model = Friend 
        fields = '__all__'

    def validate(self, args):
        user_id = args.get('user_id', None)
        friend_id = args.get('friend_id', None)

        user = User.objects.filter(id=user_id)
        friend = User.objects.filter(id=friend_id)

        if not user.exists():
            raise serializers.ValidationError({'users':('This follower is not found')})
        if not friend.exists():
            raise serializers.ValidationError({'users':('This following is not found')})
        
        return super().validate(args)
    
    def create(self, validated_data):
        user_id = validated_data['user_id']
        friend_id = validated_data['friend_id']
        
        friend_info = Friend.objects.filter(user_id=user_id, friend_id=friend_id).first()
        if friend_info is not None:
            friend_info.is_followed = not friend_info.is_followed
            friend_info.save()
            return friend_info

        new_friend = Friend.objects.create(**validated_data)
        return new_friend
       


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(required=True, allow_null=False, write_only=True)
    posts = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

    def validate(self, args):
        user_id = args.get('user_id', None)

        user = User.objects.filter(id=user_id)
        if not user.exists():
            raise serializers.ValidationError({'users':('This user is not found')})
        return super().validate(args)

    def get_posts(self, obj):
        posts = Post.objects.filter(user=obj.user).order_by('-id')
        serializer = PostSerializer(posts, many=True)
        return serializer.data
    
    def create(self, validated_data):
        return Profile.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        bio = validated_data.get('bio', instance.bio)
        url = validated_data.get('url', instance.url)

        new_avatar = validated_data.get('avatar', None)
        if new_avatar:
            instance.avatar = new_avatar

        instance.bio = bio
        instance.url = url
        instance.save()

        return instance