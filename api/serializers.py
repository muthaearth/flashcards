from rest_framework import serializers
from .models import Deck, Flashcard

""" Django rest_framework serializers https://www.django-rest-framework.org/api-guide/serializers/#modelserializer

Data within 'Deck' and 'Flashcard' querysets and model instances will be converted to python datatypes and then rendered into JSON

Example:
DeckSerializer.base_fields['description'] = DeckSerializer(many=True, allow_add_remove=True)

CardSerializer.base_fields['answer'] = CardSerializer(many=True, allow_add_remove=True)
"""


class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = ('id', 'name', 'description')


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = ('id', 'question', 'answer',
                  'easiness', 'consec_correct_answers')
        # list or tuple of field names that do not need to be updated on the card
        read_only_fields = ('created_at', 'last_shown_at', 'next_due_date')


# attributes of serialized objects saved when updated
class RatingSerializer(serializers.Serializer):
    rating = serializers.IntegerField(
        write_only=True, min_value=0, max_value=5)
    easiness = serializers.FloatField(read_only=True)
    card_created_at = serializers.IntegerField(read_only=True)
    last_shown_at = serializers.DateTimeField(read_only=True)
    next_due_date = serializers.DateTimeField(read_only=True)

    def update(self, card, validated_data):
        card.save(rating=int(validated_data['rating']))
        return card
