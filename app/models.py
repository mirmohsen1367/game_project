from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import random
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
    point = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    user_group = models.ForeignKey("app.GroheUser", on_delete=models.DO_NOTHING,
                                   related_name="users", related_query_name="user", null=True)
    leader_board = models.BigIntegerField(default=1)
    level = models.IntegerField(default=1)
    xp = models.BigIntegerField(default=0, validators=[MinValueValidator(0)])
    coin = models.BigIntegerField(default=0, validators=[MinValueValidator(0)])
    gem = models.BigIntegerField(default=0, validators=[MinValueValidator(0)])
    elixir = models.BigIntegerField(default=0, validators=[MinValueValidator(0)])
    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ('-id',)
        db_table = "user"


class UserProfile(Base):
    def file_directory_path(instance, filename):
        return 'avatar/{0}/{1}'.format(str(instance.user), "_".join([str(random.randint(0000000000, 9999999999)), filename]))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profiles")
    LEVEL = (("low", "LOW"),
             ("middel", "MIDDEL"),
             ("hight", "HIGHT"))

    nickname = models.CharField(max_length=60)
    avatar = models.FileField(upload_to=file_directory_path)

    @property
    def image_link(self):
        return f"{settings.IMAGE_URL_SERVE}{settings.MEDIA_URL}{self.avatar}"

    class Meta:
        ordering = ('-id',)
        db_table = "user_profile"


class Device(Base):

    device_id = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="device")

    class Meta:
        ordering = ('-id',)
        db_table = "device"


class GroheUser(Base):

    class Meta:
        ordering = ("id",)
        db_table = "grohe_user"


class Tournoment(Base):
    name = models.CharField(max_length=50)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    max_coin_reward = models.IntegerField()
    min_coin_reward = models.IntegerField()

    class Meta:
        ordering = ("-id",)
        db_table = "tournoment"
