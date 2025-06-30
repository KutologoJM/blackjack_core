from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.


class Player(models.Model):
    name = models.CharField(max_length=50, unique=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Hand(models.Model):
    player = models.ForeignKey(Player, related_name='hands', on_delete=models.CASCADE)
    hand_id = models.IntegerField(default=0)
    hand_total = models.IntegerField(default=0)
    current_bet = models.IntegerField(default=0)
    card_details = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list
    )
    special_condition = models.CharField(max_length=50, default='None')

    def __str__(self):
        return f"{self.player.name}'s Hand {self.hand_id}"


class Dealer(models.Model):
    is_dealer = models.BooleanField(default=True)
    hand_total = models.IntegerField(default=0)
    hole_card = models.CharField(max_length=50, blank=True)
    face_card = models.CharField(max_length=50, blank=True)
    dealer_cards = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list
    )
