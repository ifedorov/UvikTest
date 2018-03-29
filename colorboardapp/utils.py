from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def get_game_result(number_of_players, board_sequence, cards_in_deck):
    _cards = [item.strip() for item in cards_in_deck.split(',')]
    _players = range(1, number_of_players + 1)
    _player_position = dict((x, -1) for x in _players)

    for index, player, cards in player_deck_generator(_players, _cards):
        for card in cards:
            position = _player_position[player]
            _find = board_sequence.find(card, position + 1)
            if _find < 0 or _find == len(board_sequence) - 1:
                return 'Player {0} won after {1} cards.'.format(player, index + 1)
            _player_position[player] = _find

    return 'No player won after {0} cards.'.format(len(_cards))


def player_deck_generator(player, deck):
    player_index = 0
    deck_index = 0

    while deck_index < len(deck):

        if player_index >= len(player):
            player_index = 0

        yield (deck_index, player[player_index], deck[deck_index])

        player_index += 1
        deck_index += 1


def card_empty_validator(value):
    for item in value.split(','):
        tmp = item.strip()
        if not tmp:
            raise ValidationError(_("Empty card not allowed"))
    return value


def card_max_value_validator(value):
    values = value.split(',')
    if len(values) > 200:
        raise ValidationError(_("Ensure this value has at most 200 characters (%(length)s.']"),
                              params={'length': len(values)})
    return value


def card_size_validator(value):
    error_fields = []

    for item in value.split(','):
        tmp = item.strip()

        if len(tmp) > 2:
            error = ValidationError(_('%(card)s - allowed  only two-color cards'), params={'card': tmp})
            error_fields.append(error)

    if error_fields:
        raise ValidationError(error_fields)
    return value


def two_color_validator(value):
    error_fields = []

    for item in value.split(','):
        tmp = item.strip()

        if tmp and not all(x == tmp[0] for x in tmp):
            error = ValidationError(_('%(card)s - allowed  only same color for two-color cards'), params={'card': tmp})
            error_fields.append(error)

    if error_fields:
        raise ValidationError(error_fields)
