from django.contrib import admin
from .models import Follow,tags,Post,Profile

# Register your models here.
admin.site.register(Profile)
admin.site.register(tags)
admin.site.register(Follow)
admin.site.register(Post)


