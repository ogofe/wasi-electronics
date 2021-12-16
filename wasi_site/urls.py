from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve



urlpatterns = [
    path('', include('core.urls', namespace='core')),
    path('admin/', include('admin.urls', namespace='wasi_admin')),
    path('shop/', include('store.urls', namespace='store')),
    # path('media/', static),
]

if settings.DEBUG:
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
            }),
        ]
