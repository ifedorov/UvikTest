from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator, RegexValidator
from django.forms import ModelForm, CharField, NumberInput, Textarea, IntegerField
from django.utils.translation import gettext as _

from colorboardapp.models import GameResult
from colorboardapp.utils import get_game_result, card_empty_validator, card_max_value_validator, card_size_validator, \
    two_color_validator


class GameForm(ModelForm):
    number_of_players = IntegerField(widget=NumberInput(attrs={'class': 'form-control'}),
                                     validators=[MinValueValidator(1), MaxValueValidator(4)])

    number_of_squares = IntegerField(widget=NumberInput(attrs={'class': 'form-control'}),
                                     validators=[MinValueValidator(1), MaxValueValidator(79)])

    number_of_cards = IntegerField(widget=NumberInput(attrs={'class': 'form-control'}),
                                   validators=[MinValueValidator(1), MaxValueValidator(200)])
    board_sequence = CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': 4}),
                               validators=[MaxLengthValidator(79),
                                           RegexValidator(regex="^[A-Z]+$", message="Allowed only uppercase A-Z ")])

    cards_in_deck = CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': 4}),
                              validators=[card_max_value_validator,
                                          RegexValidator(regex="^[A-Z,\s]+$",
                                                         message="Allowed only uppercase A-Z comma and space"),
                                          card_empty_validator,
                                          card_size_validator,
                                          two_color_validator
                                          ])

    class Meta:
        model = GameResult
        fields = ["number_of_players", "number_of_squares", "number_of_cards", "board_sequence", "cards_in_deck"]

    def clean(self):
        cleaned_data = super(GameForm, self).clean()

        number_of_squares = cleaned_data.get("number_of_squares")
        number_of_cards = cleaned_data.get("number_of_cards")
        board_sequence = cleaned_data.get("board_sequence")
        cards_in_deck = cleaned_data.get("cards_in_deck")

        errors = []

        if board_sequence and number_of_squares != len(board_sequence):
            error = ValidationError(
                _("Board sequence (%(board_sequence_len)s) does not match number of squares (%(number_of_squares)s)"),
                params={'board_sequence_len': len(board_sequence), 'number_of_squares': number_of_squares})
            errors.append(error)

        if cards_in_deck:
            cards_in_deck_len = len(cards_in_deck.split(','))
            if number_of_cards != cards_in_deck_len:
                error = ValidationError(
                    _("Cards in deck (%(cards_in_deck_len)s) does not match number of cards (%(number_of_cards)s)"),
                    params={'cards_in_deck_len': cards_in_deck_len, 'number_of_cards': number_of_cards})
                errors.append(error)

        if errors:
            raise ValidationError(errors)

        return cleaned_data

    def save(self, commit=True):
        instance = super(GameForm, self).save(commit=False)

        instance.result = get_game_result(instance.number_of_players, instance.board_sequence, instance.cards_in_deck)
        instance.save()
        return instance
