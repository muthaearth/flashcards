from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from flashcards import views as flashcards_views

urlpatterns = [
    path('', flashcards_views.home, name="home"),
    path('', include('flashcards.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.simple.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/registration/', include('registration.backends.hmac.urls')),

    # HMAC workflow, found in registration.backends.hmac, implements a 2-step reg process(signup, followed by activation). Unlike older model-based activation workflow, it uses no models and does not store its activation key. Instead, activation key sent to the user is timestamped, HMAC-verified value.

    # Will likely not need these urls from instructor's example project
    # path('', tracker_views.homepage, name="homepage"),
    # path('timer/', tracker_views.check_timer, name="check_timer"),
    # path('timer/start/', tracker_views.start_timer, name="start_timer"),
    # path('timer/stop/', tracker_views.stop_timer, name="stop_timer"),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
