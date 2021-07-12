from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.insta, name="insta"),
    path('', views.loginPage, name='login'),
    path('index/', views.index, name="index"),
    path('newspost/', views.NewPost, name="newspost"),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    # path('like/<int:pk>', views.BlogPostLike, name='like_post')
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 


