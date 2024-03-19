import time
import random

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def add_score(self, points):
        self.score += points

class HumanPlayer(Player):
    pass

class ComputerPlayer(Player):
    def make_decision(self):
        if self.score < 100 - self.score:
            return 'roll'
        else:
            return 'hold'

class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == 'human':
            return HumanPlayer(name)
        elif player_type == 'computer':
            return ComputerPlayer(name)
        else:
            raise ValueError("Invalid player type")

class Game:
    def __init__(self, player1_type, player2_type):
        self.player1 = PlayerFactory.create_player(player1_type, "Player 1")
        self.player2 = PlayerFactory.create_player(player2_type, "Player 2")
        self.current_player = self.player1

    def play_round(self):
        decision = self.current_player.make_decision()
        if decision == 'roll':
            dice_roll = random.randint(1, 6)
            if dice_roll == 1:
                self.current_player.score = 0
                self.switch_players()
            else:
                self.current_player.add_score(dice_roll)
        elif decision == 'hold':
            self.switch_players()

    def switch_players(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def play_game(self):
        while self.player1.score < 100 and self.player2.score < 100:
            self.play_round()

class TimedGameProxy:
    def __init__(self, player1_type, player2_type):
        self.start_time = time.time()
        self.real_game = Game(player1_type, player2_type)

    def play_round(self):
        if time.time() - self.start_time > 60:
            return
        self.real_game.play_round()

    def play_game(self):
        while time.time() - self.start_time <= 60 and (self.real_game.player1.score < 100 and self.real_game.player2.score < 100):
            self.play_round()

# Example usage
def main(player1_type, player2_type, timed=False):
    if timed:
        game = TimedGameProxy(player1_type, player2_type)
    else:
        game = Game(player1_type, player2_type)
    game.play_game()
    print("Game over")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Play Pig game")
    parser.add_argument("--player1", choices=["human", "computer"], required=True, help="Type of player 1")
    parser.add_argument("--player2", choices=["human", "computer"], required=True, help="Type of player 2")
    parser.add_argument("--timed", action="store_true", help="Play a timed game")
    args = parser.parse_args()

    main(args.player1, args.player2, args.timed)