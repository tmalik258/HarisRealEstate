from django.contrib import admin
from django.contrib import messages
from django.utils.translation import gettext as _

from .models import Listing, ListingImage, Contact

# Register your models here.

class ImageInline (admin.TabularInline):
	model = ListingImage
	fk_name = 'listing'
	verbose_name_plural = _('image')


# Listing Model
class ListingAdmin (admin.ModelAdmin):
	inlines = [ImageInline]
	list_display = ('title', 'purpose', 'category', 'bedroom', 'bathroom', 'area_size', 'area_size_unit', 'is_active', 'creator', 'time_created')
	list_filter = ('purpose', 'category', 'bedroom', 'bathroom', 'area_size', 'area_size_unit', 'is_active', 'creator', 'time_created')
	empty_value_display = '-empty-'

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		if request.user.is_superuser:
			return qs

		return Listing.objects.filter(creator=request.user) or qs.none()
	
	@admin.action
	def make_active (self, request, queryset):
		queryset.update(is_active=True)
		messages.success(request, "Selected Record(s) Marked as Active Successfully !!")

	@admin.action
	def make_inactive (self, request, queryset):
		queryset.update(is_active=False)
		messages.success(request, "Selected Record(s) Marked as Inactive Successfully !!")

	actions = ['make_active', 'make_inactive']
admin.site.register(Listing, ListingAdmin)


# Contact Model
admin.site.register(Contact)