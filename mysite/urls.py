# mysite/urls.py
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url('^MSG/', include('MSG.urls')),
    url(r'^chat/', include('chat.urls')),
    url(r'^admin/', admin.site.urls)
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
