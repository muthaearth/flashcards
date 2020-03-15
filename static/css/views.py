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


# CARD_LIMIT = 5


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


# 1. Click on a deck
# 2. that returns a random flash card inside of the deck
# 3. Then display that card in the center of the screen.


# 1. Get a list of all of the cards inside of a deck
# 2. Pick a random object's primary key from that list
# 3. Pass it into the deck link

@login_required
def home(request):
    if request.method == 'GET':
        # decks = Deck.objects.filter(owner=request.user)
        decks = Deck.objects.all()

        context = {
            'user': request.user,
            'decks': decks,
        }
        return render(request, 'flashcards/index.html', context)


def flashcard_display(request, deck_slug, pk):

    decks = Deck.objects

    for deck in decks.all():
        if slugify(deck.name) == deck_slug:
            instance = deck
            break

    context = {
        'deck': instance,
        'card': instance.flashcards.get(pk=pk),
    }

    return render(request, 'flashcards/flashcard_display.html', context)


@csrf_exempt
def new_card(request):
    """
    Create new card
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = FlashCardSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    else:
        return

    # def add(request):
    #     """
    #     Add new flashcard
    #     """
    #     if request.method == 'POST':
    #         form = CardForm(request.POST)
    #         if form.is_valid():
    #             deck_name = form.cleaned_data['deck']
    #             question = form.cleaned_data['question']
    #             answer = form.cleaned_data['answer']
    #             user = request.user
    #             Flashcard.objects.create_flashcard(user=user, question=question,
    #                                                answer=answer, deck_name=deck_name)
    #             return HttpResponseRedirect(reverse('add-card'))
    #     else:
    #         form = CardForm()

    #     return render(request, 'flashcards/add.html', {'form': form})

    # @login_required
    # @ensure_csrf_cookie
    # def study(request, deck_id):
    #     """
    #     Study cards page (JS driven)
    #     """
    #     if request.method == 'GET':
    #         return render(request, 'flashcards/study.html')

    # @login_required
    # @ensure_csrf_cookie
    # def get_cards(request, deck_id):
    #     """
    #     Get cards to study (ajax)
    #     """

    #     if request.method == 'GET':
    #         cards = Flashcard.objects.filter(owner=request.user, deck=deck_id,
    #                                          next_due_date__lte=timezone.now())
    #         count = len(cards)
    #         data = {'count': count, 'cards': []}

    #         num = count if count < CARD_LIMIT else CARD_LIMIT
    #         if num:
    #             # generate list of random indexes
    #             idx = random.sample(range(count), num)
    #             for i in idx:
    #                 card = cards[i]
    #                 # split question into a word list on new line
    #                 question = '<p>' + \
    #                     '</p><p>'.join(card.question.split('\r\n'))+'</p>'
    #                 answer = '<p>' + \
    #                     '</p><p>'.join(card.answer.split('\r\n'))+'</p>'
    #                 data['cards'].append({'id': card.pk, 'question': question,
    #                                       'answer': answer})

    #         return JsonResponse(data)
    #     else:
    #         data = json.loads(str(request.body, 'utf-8'))
    #         for response in data:
    #             card = Flashcard.objects.get(
    #                 owner=request.user, pk=response['id'])
    #             card.save(rating=res['result'])

    #         return JsonResponse({'status': 'OK'})

    # @login_required
    # def delete_deck(request):
    #     """
    #     Delete deck (ajax)
    #     """
    #     if request.method == 'POST':
    #         data = json.loads(str(request.body, 'utf-8'))
    #         if 'deck_id' in data:
    #             deck = Deck.objects.get(owner=request.user, pk=data['deck_id'])
    #             deck.delete()
    #             return JsonResponse({'status': 'OK'})

    # @csrf_exempt
    # def decks_list(request):
    #     """
    #     List all decks
    #     """
    #     # get specified resource name
    #     if request.method == 'GET':
    #         if 'name' in request.GET:
    #             decks = Deck.objects.filter(
    #                 owner=request.user, name=request.GET['name'])
    #         else:
    #             # return resource name
    #             decks = Deck.objects.filter(owner=request.user)
    #         serializer = DeckSerializer(decks, many=True)
    #         return Response(serializer.data)

    #     # user send data to Deck resource
    #     elif request.method == 'POST':
    #         serializer = DeckSerializer(data=request.data)
    #         if serializer.is_valid():
    #             if request.user.is_anonymous:
    #                 return Response(serializer.errors,
    #                                 status=status.HTTP_401_UNAUTHORIZED)
    #             else:
    #                 serializer.save(owner=request.user)
    #                 return Response(serializer.data,
    #                                 status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def deck_details(request, deck_id):
    #     """
    #     Deck details
    #     """
    #     if request.method == 'GET':
    #         deck = get_object_or_404(Deck, pk=deck_id, owner=request.user)
    #         serializer = DeckSerializer(deck)
    #         return Response(serializer.data)
    #     elif request.method == 'DELETE':
    #         deck = get_object_or_404(Deck, pk=deck_id, owner=request.user)
    #         deck.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)

    # @csrf_exempt
    # def cards_list(request, deck_id):
    #     """
    #     List all flashcards
    #     """
    #     # get card list resource
    #     if request.method == 'GET':
    #         if 'days' in request.GET:
    #             cards = Flashcard.objects.get_cards_to_study(deck_id=deck_id,
    #                                                          user=request.user, days=int(request.GET['days']))
    #         else:
    #             cards = Flashcard.objects.filter(
    #                 deck__id=deck_id, deck__owner=request.user)
    #         serializer = CardSerializer(cards, many=True)
    #         return Response(serializer.data)

    #     # post data to card list resource
    #     elif request.method == 'POST':
    #         try:
    #             deck = Deck.objects.get(id=deck_id)
    #         except ObjectDoesNotExist:
    #             return Response(serializer.errors,
    #                             status=status.HTTP_401_BAD_REQUEST)

    #         serializer = CardSerializer(data=request.data)
    #         if serializer.is_valid():
    #             if request.user.is_anonymous:
    #                 return Response(serializer.errors,
    #                                 status=status.HTTP_401_UNAUTHORIZED)
    #             else:
    #                 # saves deck if user authenticated, deck id, and serialized card data has been rendered
    #                 serializer.save(owner=request.user, deck=deck)
    #                 return Response(serializer.data,
    #                                 status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_401_BAD_REQUEST)

    # def card_details(request, deck_id, card_id):
    #     """
    #     Card details
    #     """
    #     if request.method == 'GET':
    #         card = get_object_or_404(Flashcard, pk=card_id, deck__id=deck_id,
    #                                  owner=request.user)
    #         serializer = CardSerializer(card)
    #         # return deck and serialized card data
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_401_BAD_REQUEST)

    # def card_ratings(request, deck_id, card_id):
    #     """
    #     Card ratings (state)
    #     """
    #     if request.method == 'GET':
    #         card = get_object_or_404(Flashcard, pk=card_id, deck__id=deck_id,
    #                                  owner=request.user)
    #         serializer = RatingSerializer(card)
    #         return Response(serializer.data)

    #     elif request.method == 'POST':
    #         card = get_object_or_404(Flashcard, pk=card_id, deck__id=deck_id,
    #                                  owner=request.user)
    #         serializer = RatingSerializer(card, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save(rating=request.data['rating'])
    #             # return serialized item performance rating
    #             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    #         return Response(serializer.errors, status=status.HTTP_401_BAD_REQUEST)
