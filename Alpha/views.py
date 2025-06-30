import requests

from . import models
from . import serializers
from django.http import JsonResponse
from rest_framework import generics
from logic import main
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

print("Fetching gameplay value...")
"""
try:
    url = 'kutologo.test:3000/num_of_decks'
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # Optional: raises an error for bad responses
    number_of_decks = response.json()
except requests.exceptions.Timeout:
    print("Request timed out. Using fallback value.")
    number_of_decks = 8
"""
number_of_decks = 0.5
shoe = main.Shoe(num_of_decks=number_of_decks)


# Create your views here.

class Dashboard(TemplateView):
    template_name = 'Dashboard.html'


class PlayerDataDelete(generics.DestroyAPIView):
    serializer_class = serializers.PlayerSerializer
    queryset = models.Player.objects.all()
    lookup_field = 'name'


class PlayerGameData(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Player.objects.all()
    serializer_class = serializers.PlayerSerializer
    lookup_field = 'name'


class PlayerHandDataCreate(generics.CreateAPIView):
    serializer_class = serializers.HandSerializer


class PlayerHandDataRead(generics.ListAPIView):
    serializer_class = serializers.HandSerializer

    def get_queryset(self):
        player_name = self.kwargs.get('name')
        return models.Hand.objects.filter(player__name=player_name)


class PlayerHandDataEdit(generics.UpdateAPIView):
    serializer_class = serializers.HandSerializer
    lookup_field = 'hand_id'

    def get_queryset(self):
        player_name = self.kwargs.get('name')
        return models.Hand.objects.filter(player__name__iexact=player_name)


class PlayerHandDataDelete(APIView):
    def delete(self, request, name):
        hands = models.Hand.objects.filter(player__name__iexact=name)

        if not hands.exists():
            return Response({"detail": "No hands found for this player."}, status=status.HTTP_404_NOT_FOUND)

        deleted_count = hands.count()
        hands.delete()

        return Response(
            {"detail": f"Deleted {deleted_count} hand(s) for player '{name}'."},
            status=status.HTTP_204_NO_CONTENT
        )


class CreatePlayers(APIView):
    def post(self, request):
        players = request.data.get("players")
        main.Shoe.create_new_players(players)
        return Response({"message": "Players created successfully"}, status=status.HTTP_200_OK)


class StartGame(APIView):
    def post(self, request):
        player_bets = request.data.get("player_bets")
        shoe.game_initial_deal(player_bets)
        shoe.create_dealer_instance()
        return Response({"message": "Game initialized successfully."}, status=status.HTTP_200_OK)


class BettingLogicUpdate(APIView):
    def post(self, request):
        win_conditions = shoe.win_condition_calc()
        shoe.payment_manager(win_conditions=win_conditions)
        return Response({"message": "Balances updated successfully."}, status=status.HTTP_200_OK)


class HitEndpoint(APIView):
    def post(self, request):
        hand_id = request.data.get("hand_id")
        player_name = request.data.get("player_name")

        shoe.hit(player_name=player_name, hand_id=hand_id)
        return Response({"message": "Hit successfully"}, status=status.HTTP_200_OK)


class DealerLogic(APIView):
    def post(self, request):
        shoe.dealer_logic()
        return Response({"message": "Placeholder Dealer logic"}, status=status.HTTP_200_OK)