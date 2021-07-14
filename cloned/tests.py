from django.test import TestCase
from .models import Post,Profile
from django.contrib.auth.models import User


class PostTest(TestCase):
    #setup method
    def setUp(self):
        self.user = Post(title='test13')

        
    def test_instance(self):
        self.assertTrue(isinstance(self.user,Post))            
 

    def test_save(self):
        self.user.save_post()
        posts = Post.objects.all()
        self.assertTrue(len(posts) > 0)


               
    def tearDown(self):
        Post.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()
        
    def test_save_post(self):
        self.post.save_post()
        posts=Post.objects.all()
        self.assertTrue(len(posts)>0)
        
    def test_delete_post(self):
        self.post.save_post()
        self.post.delete_post()
        posts=Post.objects.all()
        self.assertTrue(len(posts)==0)
        
    def test_update_picture(self):
        self.post.save_post()
        self.post.update_post_picture(self.post.id,'test')
        updated= Post.objects.get(picture='test')
        self.assertEqual(updated.picture,'test')
            
    