
"""
flashcards URL configuration
"""

from django.contrib import admin
from django.conf import settings
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('flashcards.urls')),
    path('accounts/', include('registration.backends.default.urls')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
