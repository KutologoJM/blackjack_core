# This is a testing space for the rough overall functionality of the app
import random
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blackjack_core.settings')
django.setup()
from Alpha import models


# random.seed(11)  # for debugging


class Shoe:

    def __init__(self, num_of_decks):
        self.rank_counter_dictionary = {
            'Ace': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0,
            '9': 0, '10': 0, 'Jack': 0, 'Queen': 0, 'King': 0
        }
        self.suit_counter_dictionary = {
            'Hearts': 0, 'Diamonds': 0, 'Clubs': 0, 'Spades': 0
        }
        self.possible_ranks = list(self.rank_counter_dictionary.keys())
        self.possible_suits = list(self.suit_counter_dictionary.keys())

        self.card_rank = None
        self.suit_rank = None
        self.card_value = 0
        self.num_of_decks = num_of_decks

    def draw(self):
        while True:
            self.card_rank = random.randint(0, 12)

            if self.card_rank == 0:
                self.card_value = 11  # unless player will go bust then a = 1

            elif self.card_rank > 0:
                self.card_value = self.card_rank + 1
                if self.card_value > 10:
                    self.card_value = 10

            if self.rank_counter_dictionary[self.possible_ranks[self.card_rank]] < (self.num_of_decks * 4):
                self.rank_counter_dictionary[self.possible_ranks[self.card_rank]] += 1
                break
            elif sum(self.rank_counter_dictionary.values()) == (self.num_of_decks * 52):
                print('card ranks have run out resetting')
                for key in self.rank_counter_dictionary:
                    self.rank_counter_dictionary[key] = 0
                for key in self.suit_counter_dictionary:
                    self.suit_counter_dictionary[key] = 0
                    continue  # temporary
            else:
                continue
        while True:
            self.suit_rank = random.randint(0, 3)
            if self.suit_counter_dictionary[self.possible_suits[self.suit_rank]] < (self.num_of_decks * 13):
                self.suit_counter_dictionary[self.possible_suits[self.suit_rank]] += 1
                break
            else:
                continue
        player_draw = f"{self.possible_ranks[self.card_rank]} of {self.possible_suits[self.suit_rank]}"
        return self.card_value, player_draw

    def hit(self, player_name, hand_id):
        hand = models.Hand.objects.filter(player__name=player_name).get(hand_id=hand_id)
        card_value, player_draw = Shoe.draw(self)
        hand.hand_total += card_value
        hand.card_details.append(player_draw)
        hand.save()
        # max_hand_id = hand.objects.order_by('-hand_id').first().hand_id
        return 'placeholder hit endpoint'

    def create_new_hand(self):  # used for splitting
        pass

    def game_initial_deal(self, player_bets):
        players = models.Player.objects.values_list('name', flat=True)
        while True:
            for player_name in players:
                player = models.Player.objects.get(name=player_name)
                hand_total = 0
                player_cards = []
                player_bet = int(player_bets[player_name])
                for x in range(2):
                    card_value, player_draw = Shoe.draw(self)
                    hand_total += card_value
                    player_cards.append(player_draw)
                    print(f"Card value:{card_value}, {player_name} has drawn the {player_draw}")
                hand_details = models.Hand.objects.create(player=player, hand_id=1, hand_total=hand_total,
                                                          current_bet=player_bet, card_details=player_cards)
            break
        return 'placeholder initial deal'

    def create_dealer_instance(self):  # used for dealer setup
        hand_total = 0
        dealer_cards = []

        hole_card_value, hole_card = Shoe.draw(self)
        face_card_value, face_card = Shoe.draw(self)

        hand_total += hole_card_value
        hand_total += face_card_value

        print(f"Dealer has drawn the {face_card}")
        dealer = models.Dealer.objects.create(is_dealer=True, hand_total=hand_total, hole_card=hole_card,
                                              face_card=face_card, dealer_cards=dealer_cards)
        return 'placeholder create dealer endpoint'

    def dealer_logic(self):
        # Dealer turn starts
        dealer = models.Dealer.objects.get(is_dealer=True)
        hand_total = dealer.hand_total
        dealer_cards = dealer.dealer_cards
        while hand_total <= 16:
            card_value, dealer_draw = Shoe.draw(self)
            hand_total += card_value
            dealer_cards.append(dealer_draw)
            dealer.hand_total = hand_total
            dealer.save()
        return 'dealer logic hit endpoint'

    @staticmethod
    def create_new_players(players):  # used for adding players
        for index in range(len(players)):
            player_name = players[index]['name']
            player_wins = players[index]['wins']
            player_losses = players[index]['losses']
            player_balance = players[index]['balance']
            models.Player.objects.create(name=player_name, wins=player_wins, losses=player_losses,
                                         balance=player_balance)
        return 'placeholder create_new_players endpoint'

    @staticmethod
    def payment_manager(win_conditions):
        while True:  # run at the end of the dealer's turn to update all player balances accordingly
            # retrieves player information(
            keys = list(win_conditions.keys())
            player_bet = 0
            for i in range(len(keys)):
                player_name = (keys[i].split()[0])
                player = models.Player.objects.get(name=player_name)
                hands = models.Hand.objects.filter(player=player)
                for hand in hands:
                    # win or loss determination
                    player_bet = int(hand.current_bet)

                if win_conditions[keys[i]] == 'Win':
                    player.balance += (1 * player_bet)
                    player.wins += 1
                    player.save()
                    print(f"Player {player_name} has won ${player_bet}")

                elif win_conditions[keys[i]] == 'Loss':
                    player.balance -= (1 * player_bet)
                    player.losses += 1
                    player.save()
                    print(f"Player {player_name} has lost ${player_bet}")

                elif win_conditions[keys[i]] == 'Doubled Win':
                    total_bet = player_bet * 2
                    player.balance += (1 * total_bet)
                    player.wins += 1
                    player.save()
                    print(f"Player {player_name} has won ${total_bet}")

                elif win_conditions[keys[i]] == 'Doubled Loss':
                    total_bet = player_bet * 2
                    player.balance -= (1 * total_bet)
                    player.losses += 1
                    player.save()
                    print(f"Player {player_name} has lost ${total_bet}")

                elif win_conditions[keys[i]] == 'BlackJack':
                    player.balance += (1.5 * player_bet)
                    player.wins += 1
                    player.save()
                    print(f"Player {player_name} has won ${1.5 * player_bet}")

                elif win_conditions[keys[i]] == 'Surrendered':
                    total_bet = player_bet / 2
                    player.balance -= (1 * total_bet)
                    player.losses += 1
                    player.save()
                    print(f"Player {player_name} has lost ${player_bet / 2}")

                elif win_conditions[keys[i]] == 'Tie':
                    player.balance += (0 * player_bet)
                    player.wins += 0
                    player.losses += 0
                    player.save()
                    print(f"Player {player_name} has tied with the Dealer.")

                else:
                    print(f"Error with {player_name} at function payment_manager.")

            break
        models.Hand.objects.all().delete()
        models.Dealer.objects.all().delete()
        return 'placeholder payment_manager endpoint'

    @staticmethod
    def win_condition_calc():  # determine win or loss of players and modify data appropriately
        players = models.Player.objects.values_list('name', flat=True)
        dealer = models.Dealer.objects.get(is_dealer=True)
        dealer_score = int(dealer.hand_total)
        win_conditions = {}
        # loops over all players
        for player_name in players:
            # retrieves player information
            player = models.Player.objects.get(name=player_name)
            hands = models.Hand.objects.filter(player=player)
            for hand in hands:
                # win or loss determination
                hand_id = int(hand.hand_id)
                player_score = int(hand.hand_total)

                special_condition = hand.special_condition
                if special_condition == "Surrendered":
                    win_conditions[f"{player_name} hand {hand_id}"] = "Surrendered"
                elif special_condition == "Doubled":
                    if player_score == 21:
                        win_conditions[f"{player_name} hand {hand_id}"] = "Doubled Blackjack"
                    elif dealer_score < player_score < 21:
                        win_conditions[f"{player_name} hand {hand_id}"] = "Doubled Win"
                    elif player_score < dealer_score or player_score > 21:
                        win_conditions[f"{player_name} hand {hand_id}"] = "Doubled Loss"
                elif player_score == 21:
                    win_conditions[f"{player_name} hand {hand_id}"] = "Blackjack"
                elif dealer_score < player_score < 21:
                    win_conditions[f"{player_name} hand {hand_id}"] = "Win"
                elif player_score < dealer_score or player_score > 21:
                    win_conditions[f"{player_name} hand {hand_id}"] = "Loss"
                elif player_score == dealer_score:
                    win_conditions[f"{player_name} hand {hand_id}"] = "Tie"

                """print(player_bet)
                print(player_score)
                print(dealer_score)"""
        return win_conditions


if __name__ == "__main__":
    shoe = Shoe(4)
    shoe.create_dealer_instance()
    pass
