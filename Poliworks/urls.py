from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.conf.urls import handler404, handler500

admin.autodiscover()

urlpatterns = [
    path('file_maintenance/', admin.site.urls, name='superuser'),
    path('', include('construction.urls')),
]
handler404 = 'construction.views.my_custom_page_not_found_view'
handler500 = 'construction.views.my_custom_error_view'

urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)