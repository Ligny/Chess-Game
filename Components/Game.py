import pygame as p

from Components.Board import Board
from Components.Move import Move
from Components.Selection import Selection

from enum import Enum
from array import array

'''
State of each turn of the game
'''
class GameState(Enum):
  QUIT = 0
  BASIC = 1
  SELECT_PIECE = 2
  MOVE = 3
  UNDO_MOVE = 4


'''
Main class of the game
'''
class Game:
  '''
  Constructor
  '''
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

##################################################################

  '''
  Update the game state to quit the game loop
  '''
  def updateQuit(self):
    if self._gameState == GameState.QUIT:
      self._running = False

  '''
  Update the game state to undo the last move
  Get last move from the move log
  '''
  def updateUndoMove(self):
    if self._gameState == GameState.UNDO_MOVE and self._move._moveLog.__len__() > 0:
      self._move._currentMove = []
      self._move._possibleMove = []
      self.board._map[self._move._moveLog[-1][0]._y][self._move._moveLog[-1][0]._x] = self._move._moveLog[-1][0]._caseSelected
      self.board._map[self._move._moveLog[-1][1]._y][self._move._moveLog[-1][1]._x] = "--"
      self._move._moveLog.pop()
      self._isWhiteTurn = not self._isWhiteTurn
      self._gameState = GameState.BASIC

  '''
  Verify if the mouse selection is valid
  '''
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

  '''
  Update the game state to move the piece
  '''
  def updateMove(self):
    '''
    Make basic move
    '''
    def basicMove():
      self.board._map[self._move._currentMove[0]._y][self._move._currentMove[0]._x] = "--"
      self.board.drawAnimateMove(self.screen, self._move._currentMove, self.clock)
      self.board._map[self._move._currentMove[1]._y][self._move._currentMove[1]._x] = self._move._currentMove[0]._caseSelected
      print(self._move._currentMove[0]._caseSelected)
      print(self._move._currentMove[1]._caseSelected)
    '''
    Make Castle move
    '''
    def CastleMove(checkCastleMove):
      myY = self._move._currentMove[0]._y
      myColor = self.board._map[self._move._currentMove[0]._y][self._move._currentMove[0]._x][0]
      self.board._map[self._move._currentMove[0]._y][self._move._currentMove[0]._x] = "--"
      self.board.drawAnimateMove(self.screen, self._move._currentMove, self.clock)
      self.board._map[self._move._currentMove[1]._y][self._move._currentMove[1]._x] = self._move._currentMove[0]._caseSelected
      if checkCastleMove < 0:
        self._move._currentMove = [Selection(7, myY, myColor + 'R' ), Selection(5, myY, "--")]
      else:
        self._move._currentMove = [Selection(0, myY, myColor + 'R'), Selection(3, myY, "--")]
      self.board._map[self._move._currentMove[0]._y][self._move._currentMove[0]._x] = "--"
      self.board.drawAnimateMove(self.screen, self._move._currentMove, self.clock)
      self.board._map[self._move._currentMove[1]._y][self._move._currentMove[1]._x] = self._move._currentMove[0]._caseSelected


    if self._gameState == GameState.SELECT_PIECE:
      if self._move._possibleMove.__len__() == 0:
        self._move.regularMove(self.board._map)
      self.board.drawHighlightValidMoves(self.screen, self._move._currentMove[0], self._move._possibleMove)
    if self._gameState == GameState.MOVE:
      self._move._moveLog.append(tuple([self._move._currentMove[0], self._move._currentMove[1]]))
      checkCastleMove = self._move._currentMove[0]._x - self._move._currentMove[1]._x
      CastleMove(checkCastleMove) if abs(checkCastleMove) == 2 else basicMove()
      self._isWhiteTurn = not self._isWhiteTurn
      self._gameState = GameState.QUIT if self._move._currentMove[1]._caseSelected[1] == 'K' else GameState.BASIC
      self._move._currentMove = []
      self._move._possibleMove = []

  '''
  Promote the pawn to a queen
  '''
  def updatePromotion(self):
    myColorEndLine = 0 if self._isWhiteTurn else 7
    for i in range(8):
      if self.board._map[myColorEndLine][i][1] == 'p':
        self.board._map[myColorEndLine][i] = self.board._map[myColorEndLine][i][0] + 'Q'


  '''
  Update all elements
  '''
  def update(self):
    self.updateQuit()
    self.updateUndoMove()
    self.updateStateInputCheck()
    self.updateMove()
    self.updatePromotion()

##################################################################
  
  '''
  Handle all events
  change the game state according to the event
  '''
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

  
  '''
  Draw all elements on the screen
  '''
  def drawElements(self):
    self.board.drawBoard(self.screen)
    self.board.drawMoveLog(self.screen, self._move._moveLog, self.font)
    self.board.drawHighlightLastMove(self.screen, self._move._moveLog)
    self.board.drawPieces(self.screen)

  '''
  Main game loop
  '''
  def gameLoop(self):
    while self._running:
      self.drawElements()
      self.eventHandler()
      self.update()
      self.clock.tick(60)
      p.display.flip()