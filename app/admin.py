from django.contrib import admin
from django.contrib.admin import AdminSite
# Register your models here.
from app.models import Device, User, UserProfile, Store, Shop


class GameAdminSite(AdminSite):
    site_header = "Game Project"
    site_title = "Game Project Admin Portal"
    index_title = "Welcome To Game Project Portal"


game_admin_site =GameAdminSite(name='game_admin')


# @admin.register(Device)
# class DeviceAdmin(admin.ModelAdmin):
#     list_display = ["id", "device_id", "user"]
#     list_filter = ["user",]
#     search_fields = ('device_id', )
from django.contrib.auth.admin import UserAdmin
@admin.register(User)
class UserAmin(UserAdmin):
    list_display = ['id',  'mobile', 'username', 'is_active']
    list_display_links = ['id', 'mobile', 'username']
    search_fields = ['id', 'mobile', 'username', 'first_name', 'last_name']
    fieldsets = (
        (None, {'fields': (
            'email', 'password', 'first_name', 'last_name', 'username', 'mobile',
            'is_active', 'is_superuser',)}),)
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#
#     list_display = ["username", "point", "level", "xp", "coin", "gem", "elixir"]
#     list_filter = ["username", "level"]


@admin.register(UserProfile)
class ProfileUserAdmin(admin.ModelAdmin):
    list_display = ["id","get_user_name", "nickname", "image_link"]

    def get_user_name(self, obj):
        return obj.user.username


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "link"]


@admin.register(Shop)
class ShopeAdmin(admin.ModelAdmin):
    list_display = ["id", "store_name", "value", "pay_value", "type", "pay_type", "image_link"]

    def store_name(self, obj):
        return obj.store.name

game_admin_site.register(Device)
game_admin_site.register(UserProfile)
game_admin_site.register(Store)
game_admin_site.register(Shop)

