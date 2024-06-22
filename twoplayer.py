import random
from typing import Optional

from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame
from wingedsheep.carcassonne.carcassonne_game_state import CarcassonneGameState
from wingedsheep.carcassonne.objects.actions.action import Action
from wingedsheep.carcassonne.objects.meeple_type import MeepleType
from wingedsheep.carcassonne.tile_sets.supplementary_rules import SupplementaryRule
from wingedsheep.carcassonne.tile_sets.tile_sets import TileSet


def print_state(carcassonne_game_state: CarcassonneGameState):
    print_object = {
        "scores": {
            "player 1": carcassonne_game_state.scores[0],
            "player 2": carcassonne_game_state.scores[1]
        },
        "meeples": {
            "player 1": {
                "normal": str(carcassonne_game_state.meeples[0]) + " / " + str(carcassonne_game_state.meeples[0] + len(list(filter(lambda x: x.meeple_type == MeepleType.NORMAL or x.meeple_type == MeepleType.FARMER, game.state.placed_meeples[0])))),
                "abbots": str(carcassonne_game_state.abbots[0]) + " / " + str(carcassonne_game_state.abbots[0] + len(list(filter(lambda x: x.meeple_type == MeepleType.ABBOT, game.state.placed_meeples[0])))),
                "big": str(carcassonne_game_state.big_meeples[0]) + " / " + str(carcassonne_game_state.big_meeples[0] + len(list(filter(lambda x: x.meeple_type == MeepleType.BIG or x.meeple_type == MeepleType.BIG_FARMER, game.state.placed_meeples[0]))))
            },
            "player 2": {
                "normal": str(carcassonne_game_state.meeples[1]) + " / " + str(carcassonne_game_state.meeples[1] + len(list(filter(lambda x: x.meeple_type == MeepleType.NORMAL or x.meeple_type == MeepleType.FARMER, game.state.placed_meeples[1])))),
                "abbots": str(carcassonne_game_state.abbots[1]) + " / " + str(carcassonne_game_state.abbots[1] + len(list(filter(lambda x: x.meeple_type == MeepleType.ABBOT, game.state.placed_meeples[1])))),
                "big": str(carcassonne_game_state.big_meeples[1]) + " / " + str(carcassonne_game_state.big_meeples[1] + len(list(filter(lambda x: x.meeple_type == MeepleType.BIG or x.meeple_type == MeepleType.BIG_FARMER, game.state.placed_meeples[1]))))
            }
        }
    }

    print(print_object)


game = CarcassonneGame(
    players=2,
    tile_sets=[TileSet.BASE, TileSet.THE_RIVER, TileSet.INNS_AND_CATHEDRALS],
    supplementary_rules=[SupplementaryRule.ABBOTS, SupplementaryRule.FARMERS]
)

# Original
# while not game.is_finished():
#     player: int = game.get_current_player()
#     valid_actions: [Action] = game.get_possible_actions()
#
#     action: Optional[Action] = random.choice(valid_actions)
#     if action is not None:
#         game.step(player, action)
#     game.render()

while not game.is_finished():
    # Player 1 is computer, Player 2 is human
    player: int = game.get_current_player()
    valid_actions: [Action] = game.get_possible_actions()

    if player == 0:
        print(f"Player {player + 1}'s turn")
        valid_actions: [Action] = game.get_possible_actions()
        action: Optional[Action] = random.choice(valid_actions)
        if action is not None:
            game.step(player, action)
        game.render()
    elif player == 1:
        print(f"Player {player + 1}'s turn")
        print("Available actions:")
        for idx, action in enumerate(valid_actions):
            print(f"{idx + 1}: {action}")  # Print available actions with index

        # Prompt user to choose an action
        while True:
            try:
                action_choice = int(input("Choose an action (enter number): "))
                if 1 <= action_choice <= len(valid_actions):
                    chosen_action = valid_actions[action_choice - 1]
                    break
                else:
                    print("Invalid number")
            except ValueError:
                print("Invalid input")

        if action is not None:
            game.step(player, chosen_action)
        game.render()
    else:
        print("Another player?")

print_state(carcassonne_game_state=game.state)
input("Press Enter to continue...")
