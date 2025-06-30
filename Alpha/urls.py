# Alpha/urls.py

from django.urls import path
from . import views

"""
C
R
U
D
"""
# full path: Kutologo.test:8000/ path starts here
urlpatterns = [
    # Dashboard
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    # Phase 1 - Game initialization
    path('create/players/', views.CreatePlayers.as_view()),
    path('start/', views.StartGame.as_view()),
    # Phase 2 - player actions begin
    path('player/hit/', views.HitEndpoint.as_view()),
    # Phase 3 - Win condition determination
    path('dealer/logic/', views.DealerLogic.as_view()),
    path('end/', views.BettingLogicUpdate.as_view()),

    # Logic Management Endpoints

    # Create
    path('game/data/hand/create/', views.PlayerHandDataCreate.as_view(), name='player_hand_data_create'),
    # Read
    path('game/data/<str:name>/', views.PlayerGameData.as_view(), name='player_game_data'),
    path('game/data/<str:name>/hand/view/', views.PlayerHandDataRead.as_view(), name='player_hand_data_read'),
    # Update
    path('game/data/<str:name>/hand/<int:hand_id>/edit/', views.PlayerHandDataEdit.as_view(), name='edit-player-hand'),
    # Delete
    path('game/data/<str:name>/hand/delete/', views.PlayerHandDataDelete.as_view(), name='player_hand_data_delete'),
    path('game/data/player/<str:name>/delete/', views.PlayerDataDelete.as_view(), name='player_data_delete'),
    # Misc

]

# ADD HIT ENDPOINT AND OTHERS
