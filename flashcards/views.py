from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, routers, status
from rest_framework.response import Response
from .models import Deck, FlashCard
from .serializers import DeckSerializer, FlashCardSerializer
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework.parsers import JSONParser
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
import json
import random


# 1. Click on a deck
# 2. Return random flash card inside of the deck
# 3. Display that card in the center of the screen.

class DeckView(viewsets.ModelViewSet):
    """
    Handles routing for POST, PATCH, GET, DELETE
    """
    queryset = Deck.objects.all()
    serializer_class = DeckSerializer


class FlashCardView(viewsets.ModelViewSet):
    """
    Handles routing for POST, PATCH, GET, DELETE
    """
    queryset = FlashCard.objects.all()
    serializer_class = FlashCardSerializer


# 1. Get list of all cards inside of a deck
# 2. Pick a random object's primary key from that list
# 3. Pass it into the deck link

@login_required
def home(request):
    if request.method == 'GET':

        decks = Deck.objects.all()

        context = {
            'user': request.user,
            'decks': decks,
        }
        return render(request, 'flashcards/index.html', context)


def flashcard_display(request, deck_slug, pk):
    # Turn the text content of deck name into a slug
    decks = Deck.objects

    for deck in decks.all():
        if slugify(deck.name) == deck_slug:
            instance = deck
            break

    card = instance.flashcards.get(pk=pk)

    context = {
        'deck': instance,
        'card': card,
    }
    return render(request, 'flashcards/flashcard_display.html', context)


def correct_answer(request, deck_slug, pk):
    # Turn the text content of deck name into a slug
    decks = Deck.objects

    for deck in decks.all():
        if slugify(deck.name) == deck_slug:
            instance = deck
            break

    card = instance.flashcards.get(pk=pk)
    card.consec_correct_answers = 1
    card.save()

    context = {
        'deck': instance,
        'card': card,
    }
    return render(request, 'flashcards/correct_answer.html', context)


def incorrect_answer(request, deck_slug, pk):
    # Turn the text content of deck name into a slug
    decks = Deck.objects

    for deck in decks.all():
        if slugify(deck.name) == deck_slug:
            instance = deck
            break

    card = instance.flashcards.get(pk=pk)
    card.consec_correct_answers = 1
    card.save()

    context = {
        'deck': instance,
        'card': card,
    }
    return render(request, 'flashcards/incorrect_answer.html', context)
