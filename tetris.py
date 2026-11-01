#  Classe principal do jogo Tetris. Ela é responsável por gerenciar o estado do jogo, incluindo a grade, as peças atuais e futuras, e a lógica de movimentação e rotação das peças.
import tetriminos 
import random

class Tetris:

    DEFAULT_WIDTH: int = 10
    DEFAULT_HEIGHT: int = 18

    _TETRIMINOS:tuple[type[tetriminos.Tetrimino], ...] = (
        tetriminos.TetriminoI, 
        tetriminos.TetriminoJ, 
        tetriminos.TetriminoL, 
        tetriminos.TetriminoO, 
        tetriminos.TetriminoS, 
        tetriminos.TetriminoT, 
        tetriminos.TetriminoZ )

    def __init__(self):
        self.reset()
        self._score = 0

    @property
    def score(self) -> int:
        return self._score

    @property
    def width(self) -> int:
        return self.DEFAULT_WIDTH

    @property
    def height(self) -> int:
        return self.DEFAULT_HEIGHT

    @property
    def game_over(self) -> bool:
        return self._game_over

    @property
    def active_tetrimino(self) -> tetriminos.Tetrimino:
        return self._tetri_active

    def reset(self) -> None:
        self._grid = [[None for _ in range(self.height)] for _ in range(self.width)]
        self._game_over = False
        self._new_tetrimino()
    
    def color_at(self, column: int, row: int) -> str | None:
        if (column, row) in self._tetri_cells(self._tetri_col, self._tetri_row):
            return self._tetri_active.color
        return self._grid[column][row]

    def move_left(self) -> None:
        if self._game_over:
            return
        if self._tetri_fits(self._tetri_col -1, self._tetri_row):
            self._tetri_col -= 1

    def move_right(self) -> None:
        if self._game_over:
            return
        if self._tetri_fits(self._tetri_col + 1, self._tetri_row):
            self._tetri_col += 1

    def move_down(self) -> None:
        if self._game_over:
            return
        if self._tetri_fits(self._tetri_col, self._tetri_row + 1):
            self._tetri_row += 1
        else:
            self._lock()

    def drop(self) -> None:
        if self._game_over:
            return
        while self._tetri_fits(self._tetri_col, self._tetri_row + 1):
            self._tetri_row += 1
        self._lock()

    def rotate(self) -> None:
        if self._game_over:
            return
        self._tetri_active.right_rotate()
        if not self._tetri_fits(self._tetri_col, self._tetri_row):
            self._tetri_active.left_rotate()

    # Métodos auxiliares protegidos

    def _tetri_cells(self, col: int, row: int) -> list[tuple[int, int]]:
        coor = []
        for block in self._tetri_active.shape:
            t = (col + block.x, row + block.y)
            coor.append(t)
        return coor

    def _tetri_fits(self, col: int, row: int) -> bool:
        for block in self._tetri_cells(col, row):
            if block[0] < 0 or block[0] >= self.width or block[1] < 0 or block[1] >= self.height:
                return False
            if self._grid[block[0]][block[1]] is not None:
                return False
        return True

    def _new_tetrimino(self) -> None:
        self._tetri_active = random.choice(Tetris._TETRIMINOS)()
        self._tetri_col = (self.width - self._tetri_active.box_size) // 2
        self._tetri_row = 0
        if not self._tetri_fits(self._tetri_col, self._tetri_row):
            self._game_over = True

    def _lock(self) -> None:
        for block in self._tetri_cells(self._tetri_col, self._tetri_row):
            self._grid[block[0]][block[1]] = self._tetri_active.color
        self._clear_rows()
        self._new_tetrimino()

    def _clear_rows(self) -> None:
        r = 0
        while r < self.height:
            if all (self._grid[c][r] != None for c in range(self.width)):
                self._score += 100

                for c in range(self.width):
                    self._grid[c].pop(r)
                    self._grid[c].insert(0, None)
            else:
                r += 1 