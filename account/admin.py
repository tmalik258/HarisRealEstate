from django.contrib import admin
from django.contrib import messages
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

	list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_verified', 'is_active', 'date_joined')

	@admin.action
	def mark_active (self, request, queryset):
		queryset.update(is_active=True)
		messages.success(request, "Selected Record(s) Marked as Active Successfully !!")

	@admin.action
	def mark_inactive (self, request, queryset):
		queryset.update(is_active=False)
		messages.success(request, "Selected Record(s) Marked as Inactive Successfully !!")

	@admin.action
	def mark_is_staff_true (self, request, queryset):
		queryset.update(is_staff=True)
		messages.success(request, "Selected Record(s) Marked as Staff Successfully !!")

	@admin.action
	def mark_is_staff_false (self, request, queryset):
		queryset.update(is_staff=False)
		messages.success(request, "Selected Record(s) Unmarked as Staff Successfully !!")

	@admin.action
	def mark_verified (self, request, queryset):
		queryset.update(is_verified=True)
		messages.success(request, "Selected Record(s) Marked as Verified Successfully !!")

	@admin.action
	def mark_unverified (self, request, queryset):
		queryset.update(is_verified=False)
		messages.success(request, "Selected Record(s) Marked as Unverified Successfully !!")

	actions = ['mark_active', 'mark_inactive', 'mark_is_staff_true', 'mark_is_staff_false', 'mark_verified', 'mark_unverified']


admin.site.register(User, UserAdmin)