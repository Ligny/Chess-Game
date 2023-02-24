import sys

from Game import Game


def main():
  try:
    game: Game = Game(512, 512)
    game.gameLoop()
  except Exception as e:
    print("Error: ", e)
    sys.exit(1)


if __name__ == "__main__":
    main()
