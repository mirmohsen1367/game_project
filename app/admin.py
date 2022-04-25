from django.contrib import admin

# Register your models here.
from app.models import Device, User, UserProfile

admin.site.register(Device)
admin.site.register(User)
admin.site.register(UserProfile)