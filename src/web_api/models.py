from datetime import datetime
from django.db import models
from django.contrib.auth.models import User 

class AbstractEntity(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        return super(AbstractEntity, self).save(*args, **kwargs)

class Friend(AbstractEntity, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name= 'user_friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name= 'user_followers')
    is_followed = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)


    class Meta:
        unique_together = ['user', 'friend']
        db_table = 'friends'


class Post(AbstractEntity, models.Model):
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name= 'user_posts')
    tagged_user = models.ManyToManyField(User, related_name= 'tagged_in_posts') #checking later
    is_hidden = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'posts'

class Image(AbstractEntity,models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True, related_name= 'images')
    image = models.ImageField(null=True, blank=True, upload_to='src/images/')

    class Meta:
        db_table = 'images'

class Video(AbstractEntity,models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True, related_name= 'videos')
    video = models.FileField(null=True, blank=True, upload_to='src/videos/')

    class Meta:
        db_table = 'videos'


class Reaction(AbstractEntity,models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name= 'reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name= 'user_reacts')
    
    class Meta:
        db_table= 'reactions'


class Comment(AbstractEntity,models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name= 'comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name= 'user_comments')
    description = models.TextField()
    
    class Meta:
        db_table= 'comments'

class Share(AbstractEntity,models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name= 'shares')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name= 'user_shares')
    
    class Meta:
        db_table= 'shares'