# Block ainda não é uma peça, mas representa um bloco dos quatro blocos.
# A importação de InvalidBlockError permite usar essa exceção no block.py. Se x ou y forem negativos, o raise aciona essa exceção.
# x representa a coluna e y representa a linha do bloco dentro da caixa do tetrimino.

from exceptions import InvalidBlockError

class Block:
    def __init__(self, x: int, y: int):
        if x < 0 or y < 0:
            raise InvalidBlockError()

        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
