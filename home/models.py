from importlib.abc import Traversable
import django
from django.contrib.auth.models import (AbstractBaseUser, AbstractUser,
                                      BaseUserManager)
from django.db import models


class UsersManager(BaseUserManager):
    def create_user(self, nid, password=None):
        if not nid:
            raise ValueError('Users must have an nid address')
        user = self.model(
            nid=self.normalize_email(nid),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
class Users(AbstractBaseUser):
    user_type = (
        ('R', 'Rentee'),
        ('S', 'Spot Owner'),
    )
    nid = models.CharField("nid",max_length=30, unique=True, primary_key=True)
    name = models.CharField("name",max_length=200)
    email = models.CharField("email",max_length=200)
    password = models.CharField("password",max_length=128)
    contact = models.CharField("contact",max_length=15, null=True)
    last_login = models.DateTimeField("last_login", auto_now_add=True, null=True)
    is_owner = models.CharField("is_owner", max_length=10, choices=user_type,default='user')
    USERNAME_FIELD = 'nid'
    objects = UsersManager()
    def __str__(self):
        return self.nid

