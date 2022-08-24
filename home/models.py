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

class SpotOwner(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    spot_ids = models.ManyToManyField('Spot', blank=True)

    def __str__(self):
        return self.user.nid


class Rentee(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    rentee_balance = models.IntegerField(default=0)
    rentee_spot_ids = models.ManyToManyField('Spot', blank=True)
    rentee_transactions = models.ManyToManyField('RenteeTransaction', blank=True)

    def __str__(self):
        return self.user.nid

class Drivers(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    driver_phone = models.IntegerField(default=0)
    driver_id = models.CharField("driver_id",max_length=30, unique=True, primary_key=True)
    
class Spot(models.Model):
    spot_id = models.CharField("spot_id",max_length=30, unique=True, primary_key=True)
    # spot_name = models.CharField("spot_name",max_length=200)
    spot_road = models.CharField("spot_road",max_length=200)
    spot_area = models.CharField("spot_area",max_length=200)
    spot_house = models.CharField("spot_house",max_length=200)
    # spot_city = models.CharField("spot_city",max_length=200)
    spot_owner = models.ForeignKey(Users, on_delete=models.CASCADE,null=True,default=None)
    spot_reviews = models.ManyToManyField('Review', blank=True)
    spot_timings = models.ManyToManyField('Timing', blank=True)
    spot_maps_url = models.CharField("spot_maps_url",max_length=200,null=True)
    spot_desc = models.CharField("spot_desc",max_length=200,null=True)
    spot_number = models.CharField("spot_number",max_length=200,null=True)
    def __str__(self):
        return self.spot_id
class Review(models.Model):
    review_id = models.CharField("review_id",max_length=30, unique=True, primary_key=True)
    review_text = models.CharField("review_text",max_length=200)
    review_rating = models.IntegerField("review_rating",default=0)
    review_date = models.DateTimeField("review_date", auto_now_add=True, null=True)
    review_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    review_spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    def __str__(self):
        return self.review_id


class RenteeTransaction(models.Model):
    transaction_id = models.CharField("transaction_id",max_length=30, unique=True, primary_key=True)
    transaction_date = models.DateTimeField("transaction_date", auto_now_add=True, null=True)

class Timing(models.Model):
    timing_id = models.CharField("timing_id",max_length=30, unique=True, primary_key=True)
    timing_start = models.TimeField("timing_start")
    timing_end = models.TimeField("timing_end")
    timing_spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    def __str__(self):
        return self.timing_id