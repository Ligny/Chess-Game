class Selection:
  def __init__(self, x: int, y: int) -> None:
    self._x = x
    self._y = y
    self._isCorrect = False

  def verifySelection(self, isWhiteTurn: bool, map) -> bool:
    if self._isCorrect == False and self._x >= 0 and self._x <= 7 and self._y >= 0 and self._y <= 7:
      if (isWhiteTurn and map[self._y][self._x][0] == "w") or (not isWhiteTurn and map[self._y][self._x][0] == "b"):
        self._isCorrect = True
    return self._isCorrect