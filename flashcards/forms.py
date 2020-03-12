import datetime
from django.forms import ModelForm
from .models import Deck, FlashCard
from django.utils.translation import ugettext_lazy as _

# ModelForm: https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/


class DeckForm(ModelForm):
    model = Deck
    fields = ['name', 'description']
    labels = {
        'name': _('Deck Name: '),
        'desciption': _('Description: '),
    }

# class CardForm(forms.Form):
#     deck = forms.CharField(label='Deck', max_length=100)
#     question = forms.CharField(label='Front', widget=forms.Textarea)
#     answer = forms.CharField(label='Back', widget=forms.Textarea)


class FlashCardForm(ModelForm):
    class Meta:
        model = FlashCard
        fields = ['deck_name', 'question',
                  'answer', 'image', 'difficulty_level']
        labels = {
            'deck_name': _('Deck Name: '),
            'question': _('Question: '),
            'answer': _('Answer:'),
            'image': _('Image: '),
            'difficulty_level': _('Difficulty Level: '),
        }
