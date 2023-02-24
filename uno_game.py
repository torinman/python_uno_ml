import random  # Random is required for shuffling of the deck

deck = []  # The pile of cards to draw from/deal
hands = []  # The cards each player is holding in their hand
pile = []  # The pile of most recently played cards

no_of_players = 4  # How many players in the game.
order_of_play = 1  # The order of play. 1 means clockwise and -1 means anticlockwise.
current_colour = ""  # The colour of the card most recently played.
current_player = 3  # The index of the current player.
# Starts at 3 because of the way that the card off the top of the deck is technically "played" by the dealer.


class NoMoreCardsError(Exception):  # Define the exception used if there are no more cards left in the deck.
    # I might make this transfer all the cards in the pile to the deck first later on.
    pass  # No action is required so nothing is done


def create_deck():  # Define a function to generate the cards in the game
    global deck  # Use the global variable deck to store all the cards in
    deck = []  # Reset the deck to empty
    colours = ["r", "y", "g", "b"]  # The four colours in the game are red, yellow, green and blue
    specials = ["r", "s", "+"]  # The colour cards that aren't numbered are reverse, skip and draw 2
    for colour in colours:  # Cycle through all the colours.
        deck.append(colour + "0")  # Add a zero card for each colour
        for number in range(1, 10, 1):  # For every colour, cycle through every number except for zero
            deck += 2 * [colour + str(number)]  # Add two of every number card
        for special in specials:  # For every colour, cycle through every special colour card
            deck += 2 * [colour + special]  # Add two of every special colour card
    deck += 4 * ["ww"]  # Add four wild cards
    deck += 4 * ["w+"]  # Add four wild draw 4 cards
    random.shuffle(deck)  # Shuffle the complete deck


def deal(cards=7, players=4):  # Define a function to deal cards to every player. Default four players with seven cards
    global deck, hands  # Use the global variables deck and hands to source the cards and store what each player has
    hands = []  # Make sure that no players already have cards
    if cards * players >= len(deck):
        raise NoMoreCardsError("There are not enough cards to play")
    for hand in range(players):  # Repeat for every player
        hands.append([])  # Clear the player's current hand
        for card in range(cards):  # Repeat for every card
            draw_card(hand, cont=False)  # Add a card to the players hand


def play_card(player, card, check=True, colour=""):
    global pile, hands, order_of_play, current_player, no_of_players, current_colour
    if not check or determine_playable(player, card):
        pile.append(card)
        if check:
            hands[player].remove(card)
        else:
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
                    draw_card(player, cont=False)
                current_player += 1
                if current_player >= no_of_players:
                    current_player = 0
        else:
            if colour == "":
                colour = input("What colour? ")
            current_colour = colour
            if list(card)[1] == "+":
                for i in range(4):
                    draw_card(player, cont=False)
        current_player = player + 1
        if current_player >= no_of_players:
            current_player = 0
        if len(hands[player]) <= 0:
            print("Game won by "+str(player))
            return "win by "+str(player)
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
