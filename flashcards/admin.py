from django.contrib import admin
from .models import Deck, FlashCard, FlashCardManager


class DeckAdmin(admin.ModelAdmin):
    pass


admin.site.register(Deck, DeckAdmin)
