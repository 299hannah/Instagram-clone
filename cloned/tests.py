from django.test import TestCase
from .models import Post,Profile
from django.contrib.auth.models import User


class PostTestClass(TestCase):
    #setup method
    def setUp(self):
        self.user = User(username='test')
        self.user.save()
        self.profile_info = Profile(user=self.user,image="image.png")
        self.post = Post(name="views",caption="...",user=self.profile_info)
        
    def tearDown(self):
        Post.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()
        
    def test_instance(self):
        self.assertTrue(isinstance(self.post,Post))
            
    def test_save_post(self):
        self.post.save_post()
        posts=Post.objects.all()
        self.assertTrue(len(posts)>0)
        
    def test_delete_post(self):
        self.post.save_post()
        self.post.delete_post()
        posts=Post.objects.all()
        self.assertTrue(len(posts)==0)
        
    def test_update_caption(self):
        self.post.save_post()
        self.post.update_post_caption(self.post.id,'test')
        updated= Post.objects.get(caption='test')
        self.assertEqual(updated.caption,'test')
            
    