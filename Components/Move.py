from Components.Selection import Selection

from array import array

'''
Class to manage the move of the pieces
'''
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

  '''
  Verify if the move is possible
  '''
  def isPossibleMove(self) -> bool:
    for move in self._possibleMove:
      if move._x == self._currentMove[1]._x and move._y == self._currentMove[1]._y:
        return True
    return False

  '''
  Get all move(s) possible in a direction
  '''
  def checkAroundEachEachDirection(self, x, y, x_offset, y_offset, times, board_map):
    actual_move: array[Selection] = []
    i = 0
    check_piece = 0

    def set_selected_compare() -> int:
      if board_map[y + y_offset][x + x_offset] == "--":
        return 0
      elif board_map[y + y_offset][x + x_offset][0] != board_map[self._currentMove[0]._y][self._currentMove[0]._x][0] and board_map[y + y_offset][x + x_offset] != "--":
        return 1
      else:
        return 2

    while i != times:
      if x + x_offset < 8 and x + x_offset >= 0 and y + y_offset < 8 and y + y_offset >= 0:
        check_piece = set_selected_compare()
        if check_piece == 0 or check_piece == 1:
          actual_move.append(Selection(x + x_offset, y + y_offset, '--'))
        if check_piece == 1 or check_piece == 2:
          break
        x += x_offset
        y += y_offset
        i += 1
      else:
        break

    return actual_move

  '''
  Get all possible move for a piece
  '''
  def regularMove(self, board_map):
    self._possibleMove = self._arrayPointer[self._currentMove[0]._caseSelected[1]](board_map)

  '''
  Get all possible move for a pawn
  '''
  def pawnMove(self, board_map):
    actual_pawn_move: array[Selection] = []
    x = self._currentMove[0]._x
    y = self._currentMove[0]._y

    if self._currentMove[0]._caseSelected[0] == "w":
      if self._currentMove[0]._y == 6:
        actual_pawn_move += self.checkAroundEachEachDirection(x, y, 0, -2, 1, board_map)
      if board_map[y - 1][x] == "--":
        actual_pawn_move += self.checkAroundEachEachDirection(x, y, 0, -1, 1, board_map)
      if board_map[y - 1][x + 1][0] == 'b':
        actual_pawn_move += self.checkAroundEachEachDirection(x, y, 1, -1, 1, board_map)
      if board_map[y - 1][x - 1][0] == 'b':
        actual_pawn_move += self.checkAroundEachEachDirection(x, y, -1, -1, 1, board_map)
    else:
      if self._currentMove[0]._y == 1:
        actual_pawn_move += self.checkAroundEachEachDirection(x, y, 0, +2, 1, board_map)
      if board_map[y + 1][x] == "--":
        actual_pawn_move += self.checkAroundEachEachDirection(x, y, 0, 1, 1, board_map)
      if board_map[y + 1][x + 1][0] == 'w':
        actual_pawn_move += self.checkAroundEachEachDirection(x, y, 0, -1, 1, board_map)
      if board_map[y + 1][x - 1][0] == 'w':
        actual_pawn_move += self.checkAroundEachEachDirection(x, y, -1, 1, 1, board_map)
    return actual_pawn_move

  '''
  Get all possible move for a rook
  '''
  def rookMove(self, board_map):
    x = self._currentMove[0]._x
    y = self._currentMove[0]._y

    actual_rook_move = self.checkAroundEachEachDirection(x, y, 1, 0, -1, board_map) +\
    self.checkAroundEachEachDirection(x, y, 0, 1, -1, board_map) +\
    self.checkAroundEachEachDirection(x, y, -1, 0, -1, board_map) +\
    self.checkAroundEachEachDirection(x, y, 0, -1, -1, board_map)
    return actual_rook_move

  '''
  Get all possible move for a bishop
  '''
  def bishopMove(self, board_map):
    x = self._currentMove[0]._x
    y = self._currentMove[0]._y

    actual_bishop_move = self.checkAroundEachEachDirection(x, y, 1, 1, -1, board_map) +\
    self.checkAroundEachEachDirection(x, y, 1, -1, -1, board_map) +\
    self.checkAroundEachEachDirection(x, y, -1, 1, -1, board_map) +\
    self.checkAroundEachEachDirection(x, y, -1, -1, -1, board_map)
    return actual_bishop_move
    
  '''
  Get all possible move for a knight
  '''
  def knightMove(self, board_map):
    actual_knight_move: array[Selection] = []
    x = self._currentMove[0]._x
    y = self._currentMove[0]._y

    def checkKnightMove(x, y):
      if x >= 0 and x < 8 and y >= 0 and y < 8 and (board_map[y][x] == "--" or board_map[y][x][0] != board_map[self._currentMove[0]._y][self._currentMove[0]._x][0]):
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
    
  '''
  Get all possible move for a queen
  '''
  def queenMove(self, board_map):
    actual_queen_move = self.rookMove(board_map) + self.bishopMove(board_map)
    return actual_queen_move
    
  '''
  Get all possible move for a king
  '''
  def kingMove(self, board_map):
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

  def queenCastle(self, last_line):
    pass
    