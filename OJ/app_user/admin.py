from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from app_user.models import UserProfile
# Register your models here.

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = 'user'
    max_num = 1


class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline, ]

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)