from django.db import models


class GameResult(models.Model):
    number_of_players = models.IntegerField()
    number_of_squares = models.IntegerField()
    number_of_cards = models.IntegerField()
    board_sequence = models.CharField(max_length=100)
    cards_in_deck = models.CharField(max_length=1000)
    result = models.CharField(max_length=100)
