import pygame as p

from Components.Board import Board
from Components.Move import Move
from Components.Selection import Selection

from enum import Enum
from array import array

class GameState(Enum):
  QUIT = 0
  BASIC = 1
  SELECT_PIECE = 2
  MOVE = 3
  UNDO_MOVE = 4

class Game:
  def __init__(self, width, height) -> None:
    # pygame init
    p.init()
    self.screen: p.Surface = p.display.set_mode((width + 250, height))
    self.font = p.font.SysFont("Arial", 14, False, False)
    self.clock = p.time.Clock()

    # game init
    self.board: Board = Board(width, height)
    self._running = True
    self._isWhiteTurn = True
    self._gameState = GameState.BASIC
    self._move: Move = Move()
    self.animateMove = False
    self.check = False
    self.checkMate = False


  def checkOrCheckMate(self):
    all_enemy_move: array[Selection] = []
    list_king_move: array[Selection] = []
    enemy_char: str = "b" if self._isWhiteTurn else "w"
    color_char: str = "w" if self._isWhiteTurn else "b"
    for y in range(8):
      for x in range(8):
        piece = self.board._map[y][x]
        if piece == str(color_char + "K"):
          print("my king position: ", x, y)
          my_king_position = [x, y]
          self._move._currentMove = [Selection(x, y, piece)]
          self._move.regularMove(self.board._map)
          list_king_move = self._move._possibleMove
          self._move._possibleMove = []
          self._move._currentMove = []
        if piece[0] == enemy_char:
          self._move._currentMove = [Selection(x, y, piece)]
          self._move.regularMove(self.board._map)
          all_enemy_move += self._move._possibleMove
          self._move._possibleMove = []
          self._move._currentMove = []
    
    for move in all_enemy_move:
      for king_move in list_king_move:
        if (move._x == king_move._x and move._y == king_move._y):
          list_king_move.remove(king_move)

    print("possible move for king", list_king_move.__len__())
    if list_king_move.__len__() == 1:
      self.checkMate = True

  def drawElements(self):
    self.board.drawBoard(self.screen)
    self.board.drawMoveLog(self.screen, self._move._moveLog, self.font)
    self.board.drawHighlightLastMove(self.screen, self._move._moveLog)
    self.board.drawPieces(self.screen)

  def updateQuit(self):
    if self._gameState == GameState.QUIT:
      self._running = False

  def updateUndoMove(self):
    if self._gameState == GameState.UNDO_MOVE and self._move._moveLog.__len__() > 0:
      self._move._currentMove = []
      self._move._possibleMove = []
      self.board._map[self._move._moveLog[-1][0]._y][self._move._moveLog[-1][0]._x] = self._move._moveLog[-1][0]._caseSelected
      self.board._map[self._move._moveLog[-1][1]._y][self._move._moveLog[-1][1]._x] = "--"
      self._move._moveLog.pop()
      self._isWhiteTurn = not self._isWhiteTurn
      self._gameState = GameState.BASIC

  def updateStateInputCheck(self):
    id_move = self._move._currentMove.__len__() - 1
    if self._gameState == GameState.SELECT_PIECE and not self._move._currentMove[id_move - 1].verifySelection(self._isWhiteTurn):
      self._move._currentMove = []
      self._possibleMove = []
      self._gameState = GameState.BASIC
    elif self._gameState == GameState.MOVE and not self._move.isPossibleMove():
      self._gameState = GameState.BASIC
      self._move._currentMove = []
      self._move._possibleMove = []

  def updateMove(self):
    if self._gameState == GameState.SELECT_PIECE:
      if self._move._possibleMove.__len__() == 0:
        self._move.regularMove(self.board._map)
      self.board.drawHighlightValidMoves(self.screen, self._move._currentMove[0], self._move._possibleMove)
    if self._gameState == GameState.MOVE:
      self._move._moveLog.append(tuple([self._move._currentMove[0], self._move._currentMove[1]]))
      self.board._map[self._move._currentMove[0]._y][self._move._currentMove[0]._x] = "--"
      self.board.drawAnimateMove(self.screen, self._move._currentMove, self.clock)
      self.board._map[self._move._currentMove[1]._y][self._move._currentMove[1]._x] = self._move._currentMove[0]._caseSelected
      self._move._currentMove = []
      self._move._possibleMove = []
      self._isWhiteTurn = not self._isWhiteTurn
      # self.checkOrCheckMate()
      self._gameState = GameState.BASIC

  def eventHandler(self):
    for event in p.event.get():
      if event.type == p.QUIT:
        self._gameState = GameState.QUIT
      if event.type == p.KEYDOWN and event.key == p.K_u:
        self._gameState = GameState.UNDO_MOVE
      if event.type == p.MOUSEBUTTONDOWN:
        self._move._currentMove.append(
          Selection(
            p.mouse.get_pos()[0] // self.board._square_size,
            p.mouse.get_pos()[1] // self.board._square_size,
            self.board._map[p.mouse.get_pos()[1] // self.board._square_size][p.mouse.get_pos()[0] // self.board._square_size]
          )
        )
        if self._gameState == GameState.BASIC:
          self._gameState = GameState.SELECT_PIECE
        elif self._gameState == GameState.SELECT_PIECE:
          self._gameState = GameState.MOVE

  def update(self):
    self.updateQuit()
    self.updateUndoMove()
    self.updateStateInputCheck()
    self.updateMove()

  def gameLoop(self):
    while self._running:
      self.drawElements()
      self.eventHandler()
      self.update()
      self.clock.tick(60)
      p.display.flip()