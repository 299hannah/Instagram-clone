from django.contrib.auth.models import User
from django.http.response import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.contrib.auth.decorators import login_required
from .models import Follow, Post, Profile,  tags
from .forms import NewsPostForm,RegisterForm,LoginForm,UpdateForm,ProfileUpdateForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.db.models.base import ObjectDoesNotExist 



# Create your views here.

# @login_required(login_url = 'login')

def index(request):
 
    post_items = Post.objects.all().order_by('pub_date')


    ctx = {
        'post_items':post_items,
        }
    return render(request, 'insta.html', ctx)

def NewPost(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewsPostForm(request.POST, request.FILES)
        if form.is_valid():
            tags = form.save(commit=False)
            tags.user = current_user
            tags.save()
        return redirect('insta')

    else:
        form = NewsPostForm()
    return render(request, 'newpost.html', {"form": form})


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(request.POST)

            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was creater  for  user')
                for user in User.objects.all():
                    Profile.objects.get_or_create(user=user)
                user = form.cleaned_data.get('user')
                return redirect('login')
 
        return render(request, 'registration/reg.html', {'form':form})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')

            else:
                messages.info(request, 'Username OR Password is incorrect')

        context = {}
            
        return render(request, 'registration/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


def post_detail(request):
    return  redirect (request,'post_detail.html')







def NewPost(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewsPostForm(request.POST, request.FILES)
        if form.is_valid():
            tags = form.save(commit=False)
            tags.user = current_user
            tags.save()
        return redirect('insta')

    else:
        form = NewsPostForm()
    return render(request, 'newpost.html', {"form": form})



def follow(request,id):
    if request.method == 'GET':
        user_follow=User.objects.get(pk=id)
        follow_user=Follow(follower=request.user, followed=user_follow)
        follow_user.save()
        return redirect('user_profile' ,username=user_follow.username)
    
def unfollow(request,id):
    if request.method=='GET':
        user_unfollow=User.objects.get(pk=id)
        unfollow_user=Follow.objects.filter(follower=request.user,followed=user_unfollow)
        unfollow_user.delete()
        return redirect('user_profile' ,username=user_unfollow.username)




def profile(request):
    if request.method == 'POST':
        u_form = UpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    user_posts = Post.objects.filter(user=request.user).order_by('-pub_date')
    posts = Post.objects.filter(user=request.user).order_by('-pub_date')
    context = {
        'u_form' : u_form,
        'p_form' : p_form,
        'user_posts' : user_posts,
        'posts' : posts,
    }
    return render(request, 'profile.html', context)







def UserProfile(request):
    current_user = request.user
    user = User.objects.get(username=current_user)
    selected_user = current_user
    if selected_user == User:
        return redirect('profile',username=request.user.username)

    posts = Post.objects.filter(user = selected_user.id)
    follow = Follow.objects.filter(follower_id = selected_user.id)
    
    profile=Profile.objects.filter(user=selected_user.id)
      
    followers = Follow.objects.filter(following=user)
   
    follow_status = False
    for follower in followers:
        if user.id == follower.follower.id:
            follow_status = True
            break
        else:
            follow_status = False
  
    ctx = {
        "posts":posts,
        "profile":profile,
        "current_user":current_user,
        'selected_user':selected_user,
        'followers': followers,
        'follow_status': follow_status
        }
   
    return render(request, 'user_profile.html',ctx)







