from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import random

from app.manager import CustomUserManager
from game_pro import settings
from django.core.validators import MinValueValidator


class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, error_messages={
        'unique': _("A user with that username already exists.")})
    password = models.CharField(null=True, blank=True,  max_length=128)
    email = models.EmailField(null=True, blank=True)
    user_group = models.ForeignKey("app.GroheUser", on_delete=models.DO_NOTHING,
                                   related_name="users", related_query_name="user", null=True)
    point = models.BigIntegerField(default=0)
    level = models.IntegerField(default=1)
    xp = models.BigIntegerField(default=0, validators=[MinValueValidator(0)])
    coin = models.BigIntegerField(default=0, validators=[MinValueValidator(0)])
    gem = models.BigIntegerField(default=0, validators=[MinValueValidator(0)])
    elixir = models.BigIntegerField(default=0, validators=[MinValueValidator(0)])
    mobile = models.CharField(max_length=11)
    REQUIRED_FIELDS = ['mobile']
    objects = CustomUserManager()

    def __str__(self):
        return self.username
    class Meta:
        ordering = ('-id',)
        db_table = "user"


class UserProfile(Base):
    def file_directory_path(instance, filename):
        return 'avatar/{0}/{1}'.format(str(instance.user), "_".join([str(random.randint(0000000000, 9999999999)), filename]))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profiles")
    nickname = models.CharField(max_length=60)
    avatar = models.FileField(upload_to=file_directory_path)

    @property
    def image_link(self):
        return f"{settings.IMAGE_URL_SERVE}{settings.MEDIA_URL}{self.avatar}"

    class Meta:
        ordering = ('-id',)
        db_table = "user_profile"

    def __str__(self):
        return self.nickname


class Device(Base):

    device_id = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="device")

    class Meta:
        ordering = ('-id',)
        db_table = "device"

    def __str__(self):
        return self.device_id

class GroheUser(Base):

    class Meta:
        ordering = ("id",)
        db_table = "grohe_user"

    def __str__(self):
        return self.pk

class Tournoment(Base):
    name = models.CharField(max_length=50)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    max_coin_reward = models.BigIntegerField()
    min_coin_reward = models.BigIntegerField()

    class Meta:
        ordering = ("-id",)
        db_table = "tournoment"
    def __str__(self):
        return self.name


class Store(Base):
    name = models.CharField(max_length=60)
    link = models.URLField(max_length=200)

    class Meta:
        ordering = ("-id",)
        db_table = "store"

    def __str__(self):
        return self.name


class Shop(Base):
    TYPE = (("coin", "COIN"), ("gem", "GEM"))
    PAY_TYPE = (("coin", "COIN"), ("gem", "GEM"), ("cash", "CASH"))

    def file_directory_path(instance, filename):
        return 'shope/{0}/{1}'.format(str(instance.store),
                                       "_".join([str(random.randint(0000000000, 9999999999)), filename]))

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="shopes",
                              related_query_name="shope")
    value = models.DecimalField(max_digits=20, decimal_places=0)
    pay_value = models.DecimalField(max_digits=20, decimal_places=0, null=True, blank=True)
    type = models.CharField(max_length=25, choices=TYPE)
    pay_type = models.CharField(max_length=25, choices=PAY_TYPE)
    img = models.FileField(upload_to=file_directory_path)

    @property
    def image_link(self):
        return f"{settings.IMAGE_URL_SERVE}{settings.MEDIA_URL}{self.img}"

    class Meta:
        ordering = ("-id",)
        db_table = "shop"
