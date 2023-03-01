import pygame as p

from Selection import Selection

from array import array

class Board:
  def __init__(self, width: int, height: int) -> None:
    self._map = [
      ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
      ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
      ["--", "--", "--", "--", "--", "--", "--", "--"],
      ["--", "--", "--", "--", "--", "--", "--", "--"],
      ["--", "--", "--", "--", "--", "--", "--", "--"],
      ["--", "--", "--", "--", "--", "--", "--", "--"],
      ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
      ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    ]
    self._width: int = width
    self._height: int = height
    self._dimension: int = self._map.__len__()
    self._square_size: int = self._height // self._dimension
    self.loadImages()

  def loadImages(self) -> None:
    self.images = {}
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
      self.images[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (self._square_size, self._square_size))

  def drawBoard(self, screen: p.Surface) -> None:
    global colors
    colors = [p.Color(235,236,208,255), p.Color(119,149,86,255)]
    for row in range(self._dimension):
      for column in range(self._dimension):
        color = colors[((row + column) % 2)]
        p.draw.rect(screen, color, p.Rect(column * self._square_size, row * self._square_size, self._square_size, self._square_size))

  def drawPieces(self, screen: p.Surface) -> None:
    for row in range(self._dimension):
      for column in range(self._dimension):
        piece = self._map[row][column]
        if piece != "--":
          screen.blit(self.images[piece], p.Rect(column * self._square_size, row * self._square_size, self._square_size, self._square_size))

  def drawHighlightLastMove(self, screen: p.Surface, move_log) -> None:
    if move_log.__len__() > 0:
      last_move = move_log[-1]
      s = p.Surface((self._square_size, self._square_size))
      s.set_alpha(100)
      s.fill(p.Color('green'))
      screen.blit(s, (last_move[1]._x * self._square_size, last_move[1]._y * self._square_size))

  def drawHighlightValidMoves(self, screen: p.Surface, actual_move: Selection, move_list) -> None:
    s = p.Surface((self._square_size, self._square_size))
    s.set_alpha(100)
    s.fill(p.Color('blue'))
    screen.blit(s, (actual_move._x * self._square_size, actual_move._y * self._square_size))
    # draw valid moves
    for move in move_list:
      s = p.Surface((self._square_size, self._square_size))
      s.set_alpha(100)
      s.fill(p.Color('yellow'))
      screen.blit(s, (move._x * self._square_size, move._y * self._square_size))

  def drawAnimateMove(self, screen: p.Surface, move, clock) -> None:
    global colors
    d_col = move[1]._x - move[0]._x
    d_row = move[1]._y - move[0]._y
    frames_per_square = 10
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
    for frame in range(frame_count + 1):
      row, col = (move[0]._y + d_row * frame / frame_count, move[0]._x + d_col * frame / frame_count)
      self.drawBoard(screen)
      self.drawPieces(screen)
      color = colors[(move[1]._x + move[1]._y) % 2]
      end_square = p.Rect(move[1]._x * self._square_size, move[1]._y * self._square_size, self._square_size, self._square_size)
      p.draw.rect(screen, color, end_square)
      screen.blit(self.images[move[0]._caseSelected], p.Rect(col * self._square_size, row * self._square_size, self._square_size, self._square_size))
      p.display.flip()
      clock.tick(60)
