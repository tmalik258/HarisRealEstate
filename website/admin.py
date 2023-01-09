from django.contrib import admin

from .models import listing, User, Comments, Images, Contact

# Register your models here.

admin.site.register(User)
admin.site.register(listing)
admin.site.register(Contact)
admin.site.register(Comments)
admin.site.register(Images)