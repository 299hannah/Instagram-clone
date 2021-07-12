from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse


class Post(models.Model):
    # postid=models
    title = models.CharField(max_length=60)
    description = models.TextField()
    location = models.TextField()
    pub_date =models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to = 'insta/', blank=True)
    # video=
    message=models.TextField(max_length=500)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    # likes = models.IntegerField()
    likes = models.ManyToManyField(User, related_name='blogpost_like')

   

    def __str__(self):
        return str(self.pub_date)


class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=80, null=True, blank=True)
    profile_info = models.TextField(max_length=150, null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    favorites = models.ManyToManyField(Post)
    picture = models.ImageField(upload_to='profile_pic', blank=True, null=True)

    def create_user_prof(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    def save_user_prof(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.first_name

    class Meta:
        ordering = ['first_name']

    post_save.connect(create_user_prof, sender=User)
    post_save.connect(save_user_prof, sender=User)

class tags(models.Model):
    name=models.CharField(max_length = 30)

    def __str__(self):
        return self.name

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE,related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE,related_name='following')

class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    pub_date =models.DateTimeField()


    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.all().filter(following=user)
        for follower in followers:
            stream =Stream(post=post, user=follower, date=post.pub_date, following=user)
            stream.save()
 
post_save.connect(Stream.add_post, sender=Post)
 