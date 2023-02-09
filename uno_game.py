import random

deck = []
hands = []
pile = []

no_of_players = 4
current_player = 3
order_of_play = 1  # clockwise
current_colour = "r"


class NoMoreCardsError(Exception):
    pass


def create_deck():
    global deck
    deck = []
    colours = ["r", "y", "g", "b"]
    specials = ["r", "s", "+"]
    for colour in colours:
        deck.append(colour + "0")
        for number in range(1, 10, 1):
            deck += 2 * [colour + str(number)]
        for special in specials:
            deck += 2 * [colour + special]
    deck += 4 * ["ww"]
    deck += 4 * ["w+"]
    random.shuffle(deck)


def deal(cards=7, players=4):
    global deck, hands
    hands = []
    for hand in range(players):
        hands.append([])
        for card in range(cards):
            draw_card(hand, cont=False)


def play_card(player, card, check=True, colour=""):
    global pile, hands, order_of_play, current_player, no_of_players, current_colour
    if determine_playable(player, card) or not check:
        pile.append(card)
        try:
            hands[player].remove(card)
        except ValueError:
            deck.remove(card)
        if list(card)[0] != "w":
            current_colour = list(card)[0]
            if list(card)[1] == "r":
                order_of_play *= -1  # reverse order of play
            if list(card)[1] == "s":
                current_player += 1
                if current_player >= no_of_players:
                    current_player = 0
            if list(card)[1] == "+":
                for i in range(2):
                    draw_card(player + 1, cont=False)
                current_player += 1
                if current_player >= no_of_players:
                    current_player = 0
        else:
            if colour == "":
                colour = input("What colour? ")
            current_colour = colour
            if list(card)[1] == "+":
                for i in range(4):
                    draw_card(player + 1, cont=False)
        current_player += 1
        if current_player >= no_of_players:
            current_player = 0
    else:
        print("You can't play that card")


def determine_playable(player, card):
    global pile, hands, current_colour
    if card in hands[player] and \
            (list(card)[0] == current_colour or  # right colour
             list(card)[1] == list(pile[-1])[1] or  # right number
             (list(card)[0] == 'w' and len(hands[player]) > 1)):  # wild
        return True
    else:
        return False


def draw_card(player, cont=True):
    global current_player
    if len(deck) < 25:
        print("Ran out of cards in deck.")
        raise NoMoreCardsError("There are no more cards in the deck")
    hands[player].append(deck[0])
    deck.remove(deck[0])
    if cont:
        current_player += 1
        if current_player >= no_of_players:
            current_player = 0