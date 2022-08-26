from email.policy import default
from importlib.abc import Traversable
from random import choices
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
        ('D', 'Driver'),
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

class SpotOwner(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.user.nid


class Rentee(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    rentee_balance = models.CharField("rentee_balance", max_length=10, default=0)


    def __str__(self):
        return self.user.nid

class Drivers(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    driver_id = models.CharField("driver_id",max_length=30,null=True,default=None)
    driver_area = models.CharField("driver_area",max_length=30,null=True,default="Dhaka")
    driver_about_me = models.CharField("driver_about_me",max_length=200,null=True,default="")
    driver_experience = models.CharField("driver_experience",max_length=200,null=True,default="2")
    
    

class Spot(models.Model):
    spot_id = models.CharField("spot_id",max_length=30, unique=True, primary_key=True)
    spot_road = models.CharField("spot_road",max_length=200)
    spot_area = models.CharField("spot_area",max_length=200)
    spot_house = models.CharField("spot_house",max_length=200)
    spot_owner = models.ForeignKey(Users, on_delete=models.CASCADE,null=True,default=None)
    spot_maps_url = models.CharField("spot_maps_url",max_length=200,null=True)
    spot_desc = models.CharField("spot_desc",max_length=200,null=True)
    spot_number = models.CharField("spot_number",max_length=200,null=True)
    spot_times = models.CharField("spot_times",max_length=200,default="")
    spot_reviews = models.CharField("spot_reviews",max_length=200,default="",null=True)
    def __str__(self):
        return self.spot_id

class TimeSlots(models.Model):
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    slot_1 = models.CharField("slot_1",max_length=200,default='9:00AM-11:00AM')
    slot_2 = models.CharField("slot_2",max_length=200,default='11:00AM-1:00PM')
    slot_3 = models.CharField("slot_3",max_length=200,default='1:00PM-3:00PM')
    slot_4 = models.CharField("slot_4",max_length=200,default='3:00PM-5:00PM')

