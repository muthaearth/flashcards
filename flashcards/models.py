from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from datetime import timedelta
from django.contrib.auth import get_user_model
from users.models import User
from django.utils.text import slugify
import random


class FlashCardManager(models.Manager):
    def create_FlashCard(self, user, question, answer, deck_name):
        try:
            deck = Deck.objects.get(owner=user, name=deck_name)
        except ObjectDoesNotExist:
            deck = Deck(owner=user, name=deck_name)
            deck.save()

        self.create(owner=user, question=question, answer=answer,
                    deck=deck)
        return deck

    def get_cards_to_study(self, user, deck_id, days):
        ##import ipdb; ipdb.set_trace()
        next_due_date = timezone.now() + timedelta(days=days)
        cards = FlashCard.objects.filter(deck__id=deck_id, deck__owner=user,
                                         next_due_date__lte=next_due_date)
        return cards


class FlashCard(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    question = models.TextField(max_length=255, blank=True, null=True)
    answer = models.TextField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_shown_at = models.DateTimeField(auto_now_add=True)
    next_due_date = models.DateTimeField(default=timezone.now)
    difficulty_level = models.FloatField(default=2.5)
    consec_correct_answers = models.IntegerField(default=0)

    objects = FlashCardManager()

    def __str__(self):
        return self.question

    def get_next_due_date(self, rating):
        """ Supermemo-2 algorithm realization.
        http://www.blueraja.com/blog/477/a-better-spaced-repetition-learning-algorithm-sm2
        Args:
            difficulty_level (int) - answer rating (0=worst, 5=best)

        Returns:
            next_due_date,difficulty_level,consec_correct_answers (tuple) - information
                to update FlashCard data
        """

        correct = (rating >= 3)
        blank = (rating < 2)
        difficulty_level = self.difficulty_level - 0.8 + 0.28*rating + 0.02*rating**2
        if difficulty_level < 1.3:
            difficulty_level = 1.3
        if correct:
            consec_correct_answers = self.consec_correct_answers + 1
            interval = 6*difficulty_level**(consec_correct_answers-1)
        elif blank:
            consec_correct_answers = 0
            interval = 0
        else:
            consec_correct_answers = 0
            interval = 1

        next_due_date = timezone.now() + timedelta(days=interval)
        return next_due_date, difficulty_level, consec_correct_answers

    def save(self, rating=None, *args, **kwargs):
        if rating:
            result = self.get_next_due_date(rating)
            self.next_due_date = result[0]
            self.difficulty_level = result[1]
            self.consec_correct_answers = result[2]
        # Call the "real" save() method.
        super(FlashCard, self).save(*args, **kwargs)


class Deck(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(default='')
    flashcards = models.ManyToManyField(FlashCard)

    def __str__(self):
        return self.name

    def get_cards_num(self):
        cards = FlashCard.objects.get_cards_to_study(
            user=self.owner, deck_id=self.id, days=0)
        return len(cards)

    @property
    def slug(self):
        """Returns a slugged version of the name of the deck (e.g., Deck Name: Truthy Falsy, Slug: truthy-falsy)"""
        return slugify(self.name)

    def random_card(self):
        """Return a random primary key of a flashcard in current deck."""
        card_pk = random.choice(self.flashcards.all()).pk
        card = self.flashcards.get(pk=card_pk)
        if card.consec_correct_answers == 1 or card.consec_correct_answers == -1:
            card_pk = random.choice(self.flashcards.all()).pk
            card = self.flashcards.get(pk=card_pk)

        return card_pk


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
