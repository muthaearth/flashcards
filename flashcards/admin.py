from django.contrib import admin
from .models import Deck, FlashcardManager, Flashcard


class DeckAdmin(admin.ModelAdmin):
    pass


admin.site.register(Deck, DeckAdmin)
