from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('<slug:deck_slug>/<int:pk>/',
         views.flashcard_display, name='flashcard_display'),
    path('<slug:deck_slug>/<int:pk>/correct/',
         views.correct_answer, name='correct_answer'),
    path('<slug:deck_slug>/<int:pk>/incorrect/',
         views.incorrect_answer, name='incorrect_answer'),
#     path('<slug:deck_slug><int:pk>/correct_score/',
#          views.correct_score, name='correct_score'),
