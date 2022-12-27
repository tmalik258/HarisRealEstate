from django.contrib import admin

from .models import listing, User, Comments, Images

# Register your models here.

admin.site.register(User)
admin.site.register(listing)
# admin.site.register(Category)
admin.site.register(Comments)
admin.site.register(Images)