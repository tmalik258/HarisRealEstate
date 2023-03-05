from django.contrib import admin

from .models import listing, User, Comments, Images, Contact

# Register your models here.

admin.site.register(User)

# Listing Model
class ListingAdmin (admin.ModelAdmin):
	list_display = ('id', 'title', 'area_size', 'area_size_unit', 'active', 'creator', 'time_created')
admin.site.register(listing, ListingAdmin)

admin.site.register(Contact)
admin.site.register(Comments)
admin.site.register(Images)