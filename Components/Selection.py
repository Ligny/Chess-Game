class Selection:
  def __init__(self, x: int, y: int, case: str) -> None:
    self._x = x
    self._y = y
    self._isCorrect = False
    self._caseSelected: str = case

  def verifySelection(self, isWhiteTurn: bool) -> bool:
    if self._isCorrect == False and self._x >= 0 and self._x <= 7 and self._y >= 0 and self._y <= 7:
      if (isWhiteTurn and self._caseSelected[0] == "w") or (not isWhiteTurn and self._caseSelected[0] == "b"):
        self._isCorrect = True
    return self._isCorrect