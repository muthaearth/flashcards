from django.contrib import admin
from .models import Deck, FlashCard, FlashCardManager

admin.site.register(Deck)
admin.site.register(FlashCard)
admin.site.register(FlashCardManager)
