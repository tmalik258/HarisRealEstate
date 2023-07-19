from django.contrib import admin
from django.contrib import messages
from django.utils.translation import gettext as _

from .models import (Listing, ListingImage, Contact, Category, Amenities, ListingAmenity, ListingSpecification, ListingSpecificationValue)

# Register your models here.
admin.site.register(Amenities)
admin.site.register(ListingSpecification)


@admin.register(Category)
class CategoryAdmin (admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}


class ListingAmenityInline (admin.TabularInline):
	model = ListingAmenity
	fk_name = 'listing'
	verbose_name_plural = _('Amenities')


class ListingSpecificationInline(admin.TabularInline):
	model = ListingSpecification


class ListingSpecificationValueInline(admin.TabularInline):
	model = ListingSpecificationValue


class ImageInline (admin.TabularInline):
	model = ListingImage
	fk_name = 'listing'
	verbose_name_plural = _('image')


# Listing Model
class ListingAdmin (admin.ModelAdmin):
	inlines = [
		ListingAmenityInline,
		ImageInline,
		ListingSpecificationValueInline
	]
	list_display = ('title', 'is_active', 'area_size_unit', 'creator', 'time_created')
	list_filter = ('area_size_unit', 'is_active', 'creator', 'time_created')
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

# Image Model
class ImageAdmin (admin.ModelAdmin):
	list_display = ('listing', 'image_tag')
	list_filter = ('listing',)
admin.site.register(ListingImage, ImageAdmin)

# Contact Model
admin.site.register(Contact)