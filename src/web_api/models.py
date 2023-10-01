from datetime import datetime
from django.db import models
from django.contrib.auth.models import User 

class AbstractEntity(models.Model):
    created_at = models.DateTimeField(default=None)
    updated_at = models.DateTimeField(default=None)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(AbstractEntity, self).save(*args, **kwargs)

class Friend(AbstractEntity, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name= 'user_friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name= 'user_followers')
    is_followed = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)


    class Meta:
        unique_together = ['user', 'friend']
        db_table = 'friends'


class Post(AbstractEntity, models.Model):
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name= 'user_posts')
    is_hidden = models.BooleanField(default=False)
    count_reacts = models.IntegerField(default=0)
    parent_post = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='shares')
    
    class Meta:
        db_table = 'posts'
    
class UserTag(AbstractEntity, models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, related_name= 'user_tags')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name= 'user_tags')
    
    class Meta:
        db_table = 'usertags'


class UploadFile(AbstractEntity, models.Model):
    file = models.FileField(null=False, blank=True)
    file_type = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'files'


class PostFile(AbstractEntity, models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name= 'post_files')
    file = models.ForeignKey(UploadFile, on_delete=models.CASCADE, null=True, related_name= 'post_files')

    class Meta:
        db_table = 'posts_files'


class Reaction(AbstractEntity, models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, related_name= 'post_reacts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name= 'user_reacts')
    react_type = models.CharField(max_length=20, null=False, default= 'NOT_REACT')
    
    class Meta:
        db_table= 'reactions'


class Comment(AbstractEntity, models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, related_name= 'post_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name= 'user_comments')
    description = models.TextField()
    is_hidden = models.BooleanField(default=False)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    class Meta:
        db_table= 'comments'

class Share(AbstractEntity, models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, related_name= 'post_shares')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name= 'user_shares')
    
    class Meta:
        db_table= 'shares'

class Profile(AbstractEntity, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiles')
    url = models.URLField(max_length=1000, null=True, blank=True)
    bio = models.TextField(max_length=150, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatar', blank=True, null=True, )

    class Meta:
        db_table = 'profiles'