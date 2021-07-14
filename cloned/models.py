from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from cloudinary.models import CloudinaryField


class Post(models.Model):
    # postid=models
    title = models.CharField(max_length=60)
    description = models.TextField()
    location = models.TextField()
    pub_date =models.DateTimeField(auto_now_add=True)
    image = CloudinaryField('image')    
    # video=
    message=models.TextField(max_length=500)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    likes = models.IntegerField()
    # likes = models.ManyToManyField(User, related_name='blogpost_like')

   

    def __str__(self):
        return str(self.pub_date)


class Profile(models.Model):

    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_info = models.TextField(max_length=150, null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    picture = CloudinaryField('image')    

    def create_user_prof(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    def save_user_prof(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return str(self.user.username)

    class Meta:
        ordering = ['user']

    # @classmethod
    # def search_by_title(cls,search_term):
    #     user = cls.objects.filter(title__icontains=search_term)
    #     return user

    # post_save.connect(create_user_prof, sender=User)
    # post_save.connect(save_user_prof, sender=User)

class tags(models.Model):
    name=models.CharField(max_length = 30)

    def __str__(self):
        return self.name



class Comments(models.Model):
    comment = models.CharField(max_length=100)
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE ,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.comment} Post'
    
    def save_comment(self):
        self.save()
    
    def delete_comment(self):
        self.delete()
    
    @classmethod
    def filter_comments_by_post_id(cls, id):
        comments = Comments.objects.filter(post_id=id)
        return comments
    

    class Meta:
        ordering = ["pk"]




class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f'{self.follower} Follow'

