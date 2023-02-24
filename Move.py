
from array import array

class Selection:
  def __init__(self, x: int, y: int) -> None:
    self._x = x
    self._y = y
    self._isCorrect = False

  def verifySelection(self) -> bool:
    print("toto")
    if self._isCorrect == False and self._x >= 0 and self._x <= 7 and self._y >= 0 and self._y <= 7:
      self._isCorrect = True
    return self._isCorrect


class Move:
  def __init__(self) -> None:
    self._moveLog = []
    self._currentMove: array[Selection] = []

  def regularMove(self) -> bool:
    # check if the move is regular
    return False