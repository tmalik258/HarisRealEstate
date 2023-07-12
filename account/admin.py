from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Profile
# Register your models here.

# User Model
class UserProfileInline (admin.StackedInline):
	model = Profile
	fk_name = 'user'
	max_num = 1
	can_delete = False
	verbose_name_plural = _('profile')


class UserAdmin (UserAdmin):
	inlines = [UserProfileInline]

	list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')


admin.site.register(User, UserAdmin)