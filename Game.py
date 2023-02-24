from Board import *
from Move import *

from enum import Enum

class GameState(Enum):
  QUIT = 0
  BASIC = 1
  SELECT_PIECE = 2
  MOVE = 3


class Game:
  def __init__(self, width, height) -> None:
    # pygame init
    p.init()
    self.screen: p.Surface = p.display.set_mode((width, height))
    self.clock = p.time.Clock()

    # game init
    self.board: Board = Board(width, height)
    self._running = True
    self._isWhiteTurn = True
    self._gameState = GameState.BASIC
    self._move: Move = Move()

  def drawElements(self):
    self.board.drawBoard(self.screen)
    self.board.drawPieces(self.screen)

  def quit(self):
    if self._gameState == GameState.QUIT:
      self._running = False

  def checkSelection(self):
    id_move = self._move._currentMove.__len__() - 1
    print(self._gameState)
    if self._gameState == GameState.SELECT_PIECE and not self._move._currentMove[id_move - 1].verifySelection():
      print("bad selection")
      self._gameState = GameState.BASIC
    elif self._gameState == GameState.MOVE and not self._move._currentMove[id_move].verifySelection() and not self._move.regularMove():
      self._gameState = GameState.SELECT_PIECE

    
  def makeMove(self):
    if self._gameState == GameState.MOVE:
      self._move._moveLog.append(self._move._currentMove)
      self._move._currentMove = []
      self._isWhiteTurn = not self._isWhiteTurn
      self._gameState = GameState.BASIC


  def eventHandler(self):
    for event in p.event.get():
      if event.type == p.QUIT:
        self._gameState = GameState.QUIT
      if event.type == p.MOUSEBUTTONDOWN:
        print("pressdown")
        self._move._currentMove.append(
          Selection(
            p.mouse.get_pos()[1] // self.board._square_size,
            p.mouse.get_pos()[0] // self.board._square_size
          )
        )
        if self._gameState == GameState.BASIC:
          self._gameState = GameState.SELECT_PIECE
        elif self._gameState == GameState.SELECT_PIECE:
          self._gameState = GameState.MOVE

  def update(self):
    self.quit()
    self.checkSelection()
    self.makeMove()


  def gameLoop(self):
    while self._running:
      self.drawElements()
      self.eventHandler()
      self.update()
      self.clock.tick(60)
      p.display.flip()