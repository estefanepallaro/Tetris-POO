import tkinter as tk
from tetris import Tetris

class TetrisApp(tk.Tk):
    CELL_SIZE = 30

    def __init__(self):
        super().__init__()

        # configurações da janela
        self.title('Tetris')
        self.game = Tetris()
        self._after_id: str | None = None
        self._canvas = tk.Canvas(self, width=self.game.width * self.CELL_SIZE, height=self.game.height * self.CELL_SIZE, bg = 'black')
        self._canvas.pack(padx=10, pady=10)
        self._status = tk.Label(self, text="", font = ("Arial", 14))
        self._status.pack(pady=5)
        restart_button = tk.Button(self, text = 'Reiniciar', command = self._restart)
        restart_button.pack(pady=5)

        # botões de controle
        self.bind("<Left>", lambda _: self._play(self.game.move_left))
        self.bind("<Right>", lambda _: self._play(self.game.move_right))
        self.bind("<Down>", lambda _: self._play(self.game.move_down))
        self.bind("<Up>", lambda _: self._play(self.game.rotate))   
        self.bind("<space>", lambda _: self._play(self.game.drop))

        # inicio da partida
        self._draw()
        self._schedule_fall()

    