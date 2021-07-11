from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Post, Stream

# Create your views here.

def insta(request):
    return render(request, 'insta.html')

def index(request):

    post_items = Post.objects.all().order_by('pub_date')

    ctx = {
        'post_items':post_items
    }
    return render(request, 'insta.html', ctx)


     




