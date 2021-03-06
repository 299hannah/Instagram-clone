from django.conf import settings
from django.conf.urls.static import static
from django.contrib import auth
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
# app_name ="cloned"

urlpatterns = [
    # path('', views.insta, name="insta"),
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('index/', views.index, name="index"),
    path('newspost/', views.NewPost, name="newspost"),
    path('register/', views.register, name='register'),
    # path('logout/', views.logoutUser, name='logout',  next_page = 'index/'),
    path('logout/', auth_views.LogoutView.as_view(next_page = '/')),
    path('post_detail/', views.post_detail, name='post_detail'),
    path('profile/',views.profile,name = 'profile'),
    path('follow/<int:id>',views.follow, name='follow'),
    path('unfollow/<int:id>',views.unfollow, name='unfollow'),
    # path('search/', views.search_results, name='search_results'),


    path('user_profile/<int:id>', views.UserProfile, name='user_profile'),
    


    # path('like/<int:pk>', views.BlogPostLike, name='like_post')
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 


