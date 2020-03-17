from django.urls import include, path
from . import views
# from rest_framework import routers


urlpatterns = [
    # path('', include(router.urls)),
    path('', views.home, name="home"),
    path('<slug:deck_slug>/<int:pk>/',
         views.flashcard_display, name='flashcard_display'),
    path('<slug:deck_slug>/<int:pk>/correct/',
         views.correct_answer, name='correct_answer')
    path('<slug:deck_slug>/<int:pk>/incorrect/',
         views.incorrect_answer, name='incorrect_answer')
]

# router = routers.DefaultRouter()
# router.register('deck', views.DeckView)
# router.register('flashards', views.FlashCardView)
