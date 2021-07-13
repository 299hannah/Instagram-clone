from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Follow, Post, Profile, Stream, tags
from .forms import NewsPostForm,RegisterForm,LoginForm,UpdateForm,ProfileUpdateForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse


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
    # if request.user.is_authenticated:
    #     return redirect('index')
    # else:
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(request.POST)

            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was creater  for + user')
                for user in User.objects.all():
                    Profile.objects.get_or_create(user=user)
                user = form.cleaned_data.get('user')
                return redirect('login')
 
        return render(request, 'registration/reg.html', {'form':form})


def loginPage(request):
    # if request.user.is_authenticated:
    #     return redirect('login')
    # else:
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


# @login_required

# def BlogPostLike(request, pk):
#     post = get_object_or_404(Post, id=request.POST.get('post_id'))
#     if post.likes.filter(id=request.user.id).exists():
#         post.likes.remove(request.user)
#     else:
#         post.likes.add(request.user)

#     return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))

# class BlogPostDetailView(DetailView):
#     model = Post


#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)

#         likes_connected = get_object_or_404(BlogPost, id=self.kwargs['pk'])
#         liked = False
#         if likes_connected.likes.filter(id=self.request.user.id).exists():
#             liked = True
#         data['number_of_likes'] = likes_connected.number_of_likes()
#         data['post_is_liked'] = liked
#         return data