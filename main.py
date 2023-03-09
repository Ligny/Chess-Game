import sys

from Components.Game import Game

'''
Entry point
'''
def main():
  try:
    game: Game = Game(512, 512)
    game.gameLoop()
  except Exception as e:
    print("Error: ", e)
    sys.exit(1)

if __name__ == "__main__":
    main()
