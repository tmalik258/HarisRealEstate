from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'Haris Real Estate Administration'
admin.site.site_title = 'Site Admin'
admin.site.index_title = 'Site administration | Haris Real Estate Site Administration'
admin.site.empty_value_display = '(Empty)'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('', include('listing.urls', namespace='listing')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
