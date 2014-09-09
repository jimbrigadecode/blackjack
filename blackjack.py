from enum import Enum
from random import randrange


class Suit(Enum):
    heart = 1
    spade = 2
    diamond = 3
    club = 4


class Card:
    """Card has value and suit
    """
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        if self.value == 1:
            val = "Ace"
        elif self.value <= 10:
            val = str(self.value)
        elif self.value == 11:
            val = "Jack"
        elif self.value == 12:
            val = "Queen"
        elif self.value == 13:
            val = "King"

        if self.suit == Suit.heart:
            suit = "hearts"
        elif self.suit == Suit.spade:
            suit = "spades"
        elif self.suit == Suit.diamond:
            suit = "diamonds"
        else:
            suit = "clubs"

        return "<" + val + " of " + suit + ">"


class BJCard(Card):
    """Black Jack Card needs special form of get_value()
    """
    def get_value(self):
        if 1 < self.value < 11:
            return self.value
        elif self.value == 1:
            return 11
        else:
            return 10


class Player:
    """Card Player

    A player holds a collection of private cards and a collection of public cards.

    Attributes:
      player_num (int)
    """
    def __init__(self, player_num):
        self.player_num = player_num
        self.private_cards = []
        self.public_cards = []
        self.num_aces = 0

    def card_down(self, card):
        if card.value == 1:
            self.num_aces += 1
        self.private_cards.append(card)

    def card_up(self, card):
        if card.value == 1:
            self.num_aces += 1
        self.public_cards.append(card)

    def get_num(self):
        return self.player_num


class BJPlayer(Player):
    """Black Jack Player has special logic for get_sum()
    """
    def get_sum(self):
        current_sum = 0
        for card in self.public_cards:
            current_sum += card.get_value()
        for card in self.private_cards:
            current_sum += card.get_value()
        num_aces_used = 0

        # if there are aces to subtract out, take away 10 for each one until less than 21
        while current_sum > 21:
            if self.num_aces > num_aces_used:
                current_sum -= 10
                num_aces_used += 1
            else:
                break
        return current_sum

    def __str__(self):
        to_string = "player: " + str(self.player_num)
        num_cards = len(self.private_cards) + len(self.public_cards)
        to_string += "\nnum_cards: " + str(num_cards)
        to_string += "\nprivate: [" + ','.join(str(e) for e in self.private_cards) + "]"
        to_string += "\npublic: [" + ','.join(str(e) for e in self.public_cards) + "]"
        to_string += "\nsum: " + str(self.get_sum())
        to_string += "\n-------------------"
        return to_string


def shuffle(the_list):
    """Shuffle a list of cards.

    Iterates through the cards, picks a random one from the remaining pile and swaps it with the first element.
    """
    size = len(the_list)
    for card_num in range(size):
        rand_range = size - card_num
        top = rand_range - 1
        rand = randrange(rand_range)
        the_list[top], the_list[rand] = the_list[rand], the_list[top]

    num_cards = {
        'suit': {},
        'value': {}
    }
    for card in the_list:
        if card.value in num_cards['value']:
            num_cards['value'][card.value] += 1
        else:
            num_cards['value'][card.value] = 1
        if card.suit in num_cards['suit']:
            num_cards['suit'][card.suit] += 1
        else:
            num_cards['suit'][card.suit] = 1

    # sanity check: make sure there are 4 of each value and 13 of each suit
    for card_num in range(1, 14):
        assert num_cards['value'][card_num] == 4
    for card_num in range(1, 5):
        assert num_cards['suit'][card_num] == 13


if __name__ == "__main__":
    cards = []
    for i in range(1, 14):
        c = BJCard(Suit.club, i)
        cards.append(c)
        c = BJCard(Suit.heart, i)
        cards.append(c)
        c = BJCard(Suit.spade, i)
        cards.append(c)
        c = BJCard(Suit.diamond, i)
        cards.append(c)

    # shuffle the cards (could use random shuffle library here but I wanted to try out a shuffle strategy for fun)
    shuffle(cards)

    # dealer is player1
    dealer = BJPlayer(1)

    # 3 other players
    player2 = BJPlayer(2)
    player3 = BJPlayer(3)
    player4 = BJPlayer(4)
    players = [player2, player3, player4]

    for player in players:
        player.card_down(cards.pop())
    dealer.card_down(cards.pop())

    for player in players:
        player.card_up(cards.pop())
    dealer.card_up(cards.pop())

    for i in range(len(players)):
        player = players[i]
        print player
        while True:
            print "[h]it or [s]tay?"
            action = raw_input()
            if action == 'h':
                new_card = cards.pop()
                player.card_up(new_card)
                player_sum = player.get_sum()
                if player_sum == 21:
                    print "Dealt {card}. You win!".format(card=new_card)
                    break
                elif player.get_sum() > 21:
                    print "Dealt {card}. You went over ({sum}).".format(card=new_card, sum=player_sum)
                    break
                print player
            elif action == 's':
                break
            else:
                print "Unknown action. Please type h or s"

    # simple dealer strategy:
    # hits while s/he's under 17
    # (for more intelligence, we could do some card counting using public cards, but I never got around to that)
    while dealer.get_sum() < 17:
        dealer.card_up(cards.pop())

    print "final results:"
    dealer_sum = dealer.get_sum()
    print "dealer score: " + str(dealer_sum)
    for i in range(len(players)):
        player = players[i]
        player_sum = player.get_sum()
        if player_sum == 21 or 21 > player_sum > dealer_sum or player_sum < 21 < dealer_sum:
            print "player: " + str(player.get_num()) + " won!"
        else:
            print "player: " + str(player.get_num()) + " lost!"
