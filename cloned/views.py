from django.contrib.auth.models import User
from django.http.response import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.contrib.auth.decorators import login_required
from .models import Comments, Follow, Post, Profile,  tags
from .forms import NewsPostForm,RegisterForm,LoginForm,UpdateForm,ProfileUpdateForm,EditProfileForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.db.models.base import ObjectDoesNotExist 



# Create your views here.

@login_required(login_url = 'login')

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






def profile(request):
    current_user = request.user
    user = User.objects.get(username=current_user.username)
    profile = Profile.objects.get(user=current_user)
    # user = User.objects.get(username=username)

    # print('this is', user)
    # follow = Follow.objects.filter(follower_id = user.id)

       
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
    posts = Post.objects.filter(user=request.user).order_by('-pub_date')
    # posts = Post.objects.filter(user = user.id)

    print (posts)
    context = {
        'u_form' : u_form,
        'p_form' : p_form,
        'posts' : posts,
        'user':user,
        'profile':profile,
    }
    return render(request, 'profile.html', context)



def search_results(request):
    if 'user' in request.GET and request.GET["user"]:
        search_term = request.GET.get("user")
        searched_profiles = Profile.objects.filter(user__username__icontains=search_term).all()

        message = f"{search_term}"
        

        return render (request, 'search.html',{"message":message,"users": searched_profiles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})




def UserProfile(request, id):
    user = User.objects.get(id=id)
    # print('this is' , user)
    selected_user = user
    if selected_user == request.user:
        return redirect('profile', id=request.user.id)

    posts = Post.objects.filter(user = selected_user.id)

    follow = Follow.objects.filter(follower_id = selected_user.id)
    
    profile=Profile.objects.filter(user=selected_user.id)
      
    followers = Follow.objects.filter(followed=user.id)
   
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
       
        'selected_user':selected_user,
        'followers': followers,
        'follow_status': follow_status
        }
   
    return render(request, 'user_profile.html',ctx)

def follow(request,id):
    if request.method == 'GET':
        user_follow=User.objects.get(pk=id)
        follow_user=Follow(follower=request.user, followed=user_follow)
        follow_user.save()
        return redirect('user_profile' ,id=user_follow.id)
    
def unfollow(request,id):
    if request.method=='GET':
        user_unfollow=User.objects.get(pk=id)
        unfollow_user=Follow.objects.filter(follower=request.user,followed=user_unfollow)
        unfollow_user.delete()
        return redirect('user_profile' ,id=user_unfollow.id)


@login_required
def EditProfile(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.nick_name = form.cleaned_data.get('nick_name')
            profile.picture = form.cleaned_data.get('image')
            profile.profile_info = form.cleaned_data.get('profile_info')
            profile.save()
            return redirect('index')
    else:
        form = EditProfileForm()
    context = {
        'form':form,
    }
    return render(request, 'edit_profile.html', context)

@login_required(login_url='/accounts/login/')
def view_post(request,pk):
    post = Post.objects.get(id=pk)
    try:
        comments = Comments.filter_comments_by_post_id(pk)
        print(comments)
        
    except Comments.DoesNotExist:  
        comments = None
    
    ctx = {
        'post':post,
        "comments":comments
        }
    
    return render(request,'view_post.html',ctx)

@login_required(login_url='/accounts/login/')
def add_comment(request,post_id):
    current_user = request.user
    if request.method == 'POST':
        comment= request.POST.get('comment')
    post = Post.objects.get(id=post_id)
    user_profile = User.objects.get(username=current_user.username)
    Comments.objects.create(
         comment=comment,
         post = post,
         user=user_profile   
        )
    return redirect('view_post' ,pk=post_id)





