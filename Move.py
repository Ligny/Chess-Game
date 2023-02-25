from Selection import Selection

from array import array

class Move:
  def __init__(self) -> None:
    self._moveLog: array[array[Selection, Selection]] = []
    self._currentMove: array[Selection] = []

  def regularMove(self) -> bool:
    # check if the move is regular
    return True

  def makeMove(self, map) -> None:
    self._moveLog.append(tuple([self._currentMove[0], self._currentMove[1]]))
    map[self._currentMove[1]._y][self._currentMove[1]._x] = map[self._currentMove[0]._y][self._currentMove[0]._x]
    map[self._currentMove[0]._y][self._currentMove[0]._x] = "--"