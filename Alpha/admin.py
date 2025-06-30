from django.contrib import admin
from django import forms
from .models import Player, Hand, Dealer  # Add any models you want admin access to


# Register your models here.

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'wins', 'losses', 'balance')


@admin.register(Hand)
class HandAdmin(admin.ModelAdmin):
    list_display = ('player', 'hand_id', 'hand_total', 'card_details', 'current_bet')


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ('is_dealer', 'hand_total', 'hole_card', 'face_card', 'dealer_cards')
