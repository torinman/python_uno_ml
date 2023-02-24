import uno_game
import uno_ml_strategies
import datetime
import random

game_data = []
games = 100

for game in range(games):
    uno_game.create_deck()
    uno_game.deal(7, uno_game.no_of_players)

    game_data.append({"players": uno_game.no_of_players, "deck": uno_game.deck, "hands": uno_game.hands, "goes": []})
    colour = random.choice(["r", "y", "g", "b"])
    game_data[game]["goes"].append(tuple((uno_game.current_player, uno_game.deck[-1], False, colour)))
    uno_game.play_card(uno_game.current_player, uno_game.deck[-1], check=False,
                       colour=colour)
    game_won = False
    while not game_won:
        game_won = True

filename = "uno_game_data_"+str(datetime.datetime.now())+".json"
with open(filename, "w") as f:
    f.write(str(game_data).replace("}", "}\n"))
