from Selection import Selection

from array import array

class Move:
  def __init__(self) -> None:
    self._moveLog: array[array[Selection, Selection]] = []
    self._currentMove: array[Selection] = []
    self._possibleMove: array[Selection] = []
    self._arrayPointer: dict[str, function] = {
      "p": self.pawnMove,
      "R": self.rookMove,
      "B": self.bishopMove,
      "N": self.knightMove,
      "Q": self.queenMove,
      "K": self.kingMove
    }

  def isPossibleMove(self) -> bool:
    for move in self._possibleMove:
      if move._x == self._currentMove[1]._x and move._y == self._currentMove[1]._y:
        return True
    return False

  def checkAroundEachEachDirection(self, x, y, x_offset, y_offset, times, board_map):
    actual_move: array[Selection] = []
    i = 0
    while i != times:
      if x + x_offset < 8 and x + x_offset >= 0 and y + y_offset < 8 and y + y_offset >= 0 and board_map[y + y_offset][x + x_offset] == "--":
        actual_move.append(Selection(x + x_offset, y + y_offset, '--'))
        x += x_offset
        y += y_offset
        i += 1
      else:
        break
    return actual_move

  def regularMove(self, board_map):
    self._possibleMove = self._arrayPointer[self._currentMove[0]._caseSelected[1]](board_map)

  def pawnMove(self, board_map):
    actual_pawn_move: array[Selection] = []
    # basic pawn move
    if self._currentMove[0]._caseSelected[0] == "w":
      if self._currentMove[0]._y == 6:
        actual_pawn_move.append(Selection(self._currentMove[0]._x, self._currentMove[0]._y - 1, '--'))
      actual_pawn_move.append(Selection(self._currentMove[0]._x, self._currentMove[0]._y - 2, '--'))
    else:
      if self._currentMove[0]._y == 1:
        actual_pawn_move.append(Selection(self._currentMove[0]._x, self._currentMove[0]._y + 2, '--'))
      actual_pawn_move.append(Selection(self._currentMove[0]._x, self._currentMove[0]._y + 1, '--'))
    return actual_pawn_move


  def rookMove(self, board_map):
    # basic rook move
    x = self._currentMove[0]._x
    y = self._currentMove[0]._y
      
    actual_rook_move = self.checkAroundEachEachDirection(x, y, 1, 0, -1, board_map) +\
    self.checkAroundEachEachDirection(x, y, 0, 1, -1, board_map) +\
    self.checkAroundEachEachDirection(x, y, -1, 0, -1, board_map) +\
    self.checkAroundEachEachDirection(x, y, 0, -1, -1, board_map)
    return actual_rook_move

  def bishopMove(self, board_map):
    # basic bishop move
    x = self._currentMove[0]._x
    y = self._currentMove[0]._y

    actual_bishop_move = self.checkAroundEachEachDirection(x, y, 1, 1, -1, board_map) +\
    self.checkAroundEachEachDirection(x, y, 1, -1, -1, board_map) +\
    self.checkAroundEachEachDirection(x, y, -1, 1, -1, board_map) +\
    self.checkAroundEachEachDirection(x, y, -1, -1, -1, board_map)
    return actual_bishop_move
    

  def knightMove(self, board_map):
    # basic knight move
    actual_knight_move: array[Selection] = []
    x = self._currentMove[0]._x
    y = self._currentMove[0]._y

    def checkKnightMove(x, y):
      if x >= 0 and x < 8 and y >= 0 and y < 8 and board_map[y][x] == "--":
        actual_knight_move.append(Selection(x, y, '--'))

    checkKnightMove(x + 1, y + 2)
    checkKnightMove(x + 1, y - 2)
    checkKnightMove(x - 1, y + 2)
    checkKnightMove(x - 1, y - 2)
    checkKnightMove(x + 2, y + 1)
    checkKnightMove(x + 2, y - 1)
    checkKnightMove(x - 2, y + 1)
    checkKnightMove(x - 2, y - 1)
    return actual_knight_move
    

  def queenMove(self, board_map):
    # basic queen move
    actual_queen_move = self.rookMove(board_map) + self.bishopMove(board_map)
    return actual_queen_move
    

  def kingMove(self, board_map):
    # basic king move
    x = self._currentMove[0]._x
    y = self._currentMove[0]._y
    actual_king_move = self.checkAroundEachEachDirection(x, y, 1, 0, 1, board_map) +\
    self.checkAroundEachEachDirection(x, y, 0, 1, 1, board_map) +\
    self.checkAroundEachEachDirection(x, y, -1, 0, 1, board_map) +\
    self.checkAroundEachEachDirection(x, y, 0, -1, 1, board_map) +\
    self.checkAroundEachEachDirection(x, y, 1, 1, 1, board_map) +\
    self.checkAroundEachEachDirection(x, y, 1, -1, 1, board_map) +\
    self.checkAroundEachEachDirection(x, y, -1, 1, 1, board_map) +\
    self.checkAroundEachEachDirection(x, y, -1, -1, 1, board_map)
    return actual_king_move
    