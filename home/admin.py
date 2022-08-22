from django.contrib import admin
from .models import *
from home.models import Users
from django.contrib import admin
from django.contrib.auth.models import User
# Register your models here.
admin.site.register(Users)
admin.site.register(User)
