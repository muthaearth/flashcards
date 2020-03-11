from django.conf.urls import url
from api import views as api_views
from rest_framework.authtoken import views


urlpatterns = [
    path('decks/$', api_views.decks_list, name='decks-list'),
    path('decks/(?P<deck_id>[0-9]+)/$',
         api_views.deck_details, name='deck-details'),
    path('decks/(?P<deck_id>[0-9]+)/cards/$',
         api_views.cards_list, name='cards-list'),
    path('decks/(?P<deck_id>[0-9]+)/cards/(?P<card_id>[0-9]+)/$',
         api_views.card_details, name='card-details'),
    path('decks/(?P<deck_id>[0-9]+)/cards/(?P<card_id>[0-9]+)/ratings/$',
         api_views.card_ratings, name='card-ratings'),
    path('api-token-auth/', views.obtain_auth_token, name='get-token')

]
