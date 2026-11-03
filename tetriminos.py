# TetriminoShape define que toda forma de tetrimino possui quatro objetos Block.
# ABC define Tetrimino como uma classe abstrata, que serve como base para os outros tetriminos.
# initial_rotation define a rotação inicial do tetrimino.
# As rotações são: 0 = inicial, 1 = 90°, 2 = 180° e 3 = 270°.
# __init__ inicializa o tetrimino, verifica sua rotação e cria suas quatro formas possíveis.
# _original_shape define a forma original de cada tetrimino e deve ser implementada pelas subclasses.
# _box_size representa o tamanho da caixa necessária para armazenar o tetrimino.
# Para calcular _box_size, é encontrado o maior valor entre x e y dos quatro blocos e depois é somado 1.
# _rotate_shape é staticmethod porque não precisa usar self para realizar a rotação.
# _rotate_shape gira uma forma 90° no sentido horário usando (box_size - 1 - y, x).
# _shapes armazena as quatro rotações possíveis do tetrimino.
# shape retorna a forma correspondente à rotação atual.
# box_size retorna o tamanho da caixa do tetrimino.
# current_rotation retorna a rotação atual do tetrimino.
# right_rotate gira o tetrimino 90° para a direita.
# left_rotate gira o tetrimino 90° para a esquerda.
# O operador % 4 mantém a rotação dentro dos valores 0, 1, 2 e 3.
# color é uma propriedade abstrata porque cada tetrimino possui sua própria cor.
# __str__ desenha o tetrimino em formato de texto dentro de sua caixa.
# Dentro de __str__, ⬜ representa uma posição ocupada e ⬛ representa uma posição vazia.


from abc import ABC, abstractmethod
from block import Block
from exceptions import InvalidRotationError

TetriminoShape = tuple[Block, Block, Block, Block]

class Tetrimino(ABC):


    def __init__(self, initial_rotation: int = 0):
        if initial_rotation < 0 or initial_rotation >= 4:
            raise InvalidRotationError()

        self._rotation = initial_rotation

        original_shape = self._original_shape()

        self._box_size = 1 + max(
            max(block.x, block.y)
            for block in original_shape
        )

        shape0 = original_shape
        shape1 = self._rotate_shape(shape0, self._box_size)
        shape2 = self._rotate_shape(shape1, self._box_size)
        shape3 = self._rotate_shape(shape2, self._box_size)

        self._shapes = (
            shape0,
            shape1,
            shape2,
            shape3
        )

    @abstractmethod
    def _original_shape(self) -> TetriminoShape:
        pass

    @staticmethod
    def _rotate_shape(shape, box_size) -> TetriminoShape:
        return tuple(
            Block(box_size - 1 - block.y, block.x)
            for block in shape
        )

    @property
    def shape(self) -> TetriminoShape:
        return self._shapes[self._rotation]

    @property
    def box_size(self) -> int:
        return self._box_size

    @property
    def current_rotation(self) -> int:
        return self._rotation

    def right_rotate(self):
        self._rotation = (self._rotation + 1) % 4

    def left_rotate(self):
        self._rotation = (self._rotation - 1) % 4

    @property
    @abstractmethod
    def color(self) -> str:
        pass

    def __str__(self) -> str:
        linhas = []

        for y in range(self._box_size):
            linha = ""

            for x in range(self._box_size):
                ocupado = any(
                    block.x == x and block.y == y
                    for block in self.shape
                )

                if ocupado:
                    linha += "⬜"
                else:
                    linha += "⬛"

            linhas.append(linha)

        return "\n".join(linhas)


# Classes dos Tetriminos
# TretiminoI
# TetriminoJ
# TetriminoL
# TetriminoO
# TetriminoS
# TetriminoT
# TetriminoZ

class TetriminoI(Tetrimino):

    def _original_shape(self) -> TetriminoShape:
        return (
            Block(0, 1),
            Block(1, 1),
            Block(2, 1),
            Block(3, 1)
        )
    @property
    def color(self) -> str:
        return "#00f0f0"

class TetriminoJ(Tetrimino):

    def _original_shape(self) -> TetriminoShape:
        return (
            Block(0, 0),
            Block(0, 1),
            Block(1, 1),
            Block(2, 1)
        )
    @property
    def color(self) -> str:
        return "#0000f0"

class TetriminoL(Tetrimino):

    def _original_shape(self) -> TetriminoShape:
        return (
            Block(2, 0),
            Block(0, 1),
            Block(1, 1),
            Block(2, 1)
        )
    @property
    def color(self) -> str:
        return "#f0a000"

class TetriminoO(Tetrimino):

    def _original_shape(self) -> TetriminoShape:
        return (
            Block(0, 0),
            Block(1, 0),
            Block(0, 1),
            Block(1, 1)
        )
    @property
    def color(self) -> str:
        return "#f0f000"

class TetriminoS(Tetrimino):

    def _original_shape(self) -> TetriminoShape:
        return (
            Block(1, 0),
            Block(2, 0),
            Block(0, 1),
            Block(1, 1)
        )
    @property
    def color(self) -> str:
        return "#00f000"

class TetriminoT(Tetrimino):

    def _original_shape(self) -> TetriminoShape:
        return (
            Block(1, 0),
            Block(0, 1),
            Block(1, 1),
            Block(2, 1)
        )
    @property
    def color(self) -> str:
        return "#a000f0"

class TetriminoZ(Tetrimino):

    def _original_shape(self) -> TetriminoShape:
        return (
            Block(0, 0),
            Block(1, 0),
            Block(1, 1),
            Block(2, 1),
        )
    @property
    def color(self) -> str:
        return "#f00000"