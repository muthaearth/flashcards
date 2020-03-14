
from django.contrib import admin
from django.conf import settings
from django.urls import include, path
# from flashcards import views as flashcard_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('flashcards.urls')),
    # path('', flashcard_views.home, name='home'),
    # path('api/', include('flashcards.urls')),
    # path('new_card/', flashcard_views.new_card, name='new_card'),
    path('accounts/', include('registration.backends.default.urls')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
