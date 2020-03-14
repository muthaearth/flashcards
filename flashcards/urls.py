from django.urls import include, path
from . import views
from rest_framework import routers


# router = routers.DefaultRouter()
# router.register('deck', views.DeckView)
# router.register('flashards', views.FlashCardView)


urlpatterns = [
    # path('', include(router.urls)),
    path('', views.home, name="home"),
    path('<slug:deck_slug>/flash-cards/',
         views.flashcard_index, name='flashcard_index')
]


# urlpatterns = [
#     path('decks/$', api_views.decks_list, name='decks-list'),
#     path('decks/(?P<deck_id>[0-9]+)/$',
#          api_views.deck_details, name='deck-details'),
#     path('decks/(?P<deck_id>[0-9]+)/cards/$',
#          api_views.cards_list, name='cards-list'),
#     path('decks/(?P<deck_id>[0-9]+)/cards/(?P<card_id>[0-9]+)/$',
#          api_views.card_details, name='card-details'),
#     path('decks/(?P<deck_id>[0-9]+)/cards/(?P<card_id>[0-9]+)/ratings/$',
#          api_views.card_ratings, name='card-ratings'),
#     path('api-token-auth/', views.obtain_auth_token, name='get-token')

# ]
