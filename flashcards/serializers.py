from rest_framework import serializers
from .models import Deck, FlashCard, FlashCardManager


class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = '__all__'


class FlashCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashCard
        fields = ('id', 'question', 'answer',
                  'easiness', 'consec_correct_answers')
        # list or tuple of field names that do not need to be updated on the card
        read_only_fields = ('created_at', 'last_shown_at', 'next_due_date')


# attributes of serialized objects saved when updated
class FlashCardManagerSerializer(serializers.Serializer):
    model = FlashCardManager
    rating = serializers.IntegerField(
        write_only=True, min_value=0, max_value=5)
    easiness = serializers.FloatField(read_only=True)
    card_created_at = serializers.IntegerField(read_only=True)
    last_shown_at = serializers.DateTimeField(read_only=True)
    next_due_date = serializers.DateTimeField(read_only=True)

    def update(self, card, validated_data):
        card.save(rating=int(validated_data['rating']))
        return card
