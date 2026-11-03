import tkinter as tk
from tetris import Tetris
from collections.abc import Callable

class TetrisApp(tk.Tk):
    CELL_SIZE = 35

    def __init__(self):
        super().__init__()

        # configurações da janela
        self.title('Tetris')

        # letreiro
        painel_titulo = tk.Frame(self)
        painel_titulo.pack(pady=10)
        letras_cores = [
            ("T", "#f00000"), # Vermelho
            ("E", "#f06800"), # Laranja
            ("T", "#f0f000"), # Amarelo
            ("R", "#00f000"), # Verde
            ("I", "#00f0f0"), # Ciano
            ("S", "#a000f0")  # Roxo
        ]
        for letra, cor in letras_cores:
            lbl = tk.Label(
                painel_titulo, 
                text=letra, 
                font=("Arial", 36, "bold"),
                fg=cor,                      
            )
            lbl.pack(side=tk.LEFT)
            
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

    def _play(self, move: Callable[[], None]):
        move()
        self._draw()

    def _schedule_fall(self):
        velocidade = max(100, 800 - (self.game.score // 500) * 50)
        self._after_id = self.after(velocidade, self._fall)
        
    def _fall(self):
        if not self.game.game_over:
            self.game.move_down()
            self._draw()
            self._schedule_fall()

    def _restart(self):
        if self._after_id is not None:
            self.after_cancel(self._after_id)
        self.game.reset()
        self._status.config(text="")
        self._draw()
        self._schedule_fall()

    def _draw(self):
        self._canvas.delete("all")

        # sombra
        sombra = self.game.ghost_cells() if not self.game.game_over else set()
        cor_ativa = self.game.active_tetrimino.color
        r = int(int(cor_ativa[1:3], 16) * 0.3 + 255 * 0.7)
        g = int(int(cor_ativa[3:5], 16) * 0.3 + 255 * 0.7)
        b = int(int(cor_ativa[5:7], 16) * 0.3 + 255 * 0.7)
        cor_sombra = f"#{r:02x}{g:02x}{b:02x}"

        for col in range(self.game.width):
            for row in range(self.game.height):
                color = self.game.color_at(col, row)

                if color is not None:
                    # bloco normal
                    self._canvas.create_rectangle(
                        col * self.CELL_SIZE,
                        row * self.CELL_SIZE,
                        (col + 1) * self.CELL_SIZE,
                        (row + 1) * self.CELL_SIZE,
                        fill=color,
                        outline="black"
                    )
                elif (col, row) in sombra:
                    # sombra translúcida
                    self._canvas.create_rectangle(
                        col * self.CELL_SIZE,
                        row * self.CELL_SIZE,
                        (col + 1) * self.CELL_SIZE,
                        (row + 1) * self.CELL_SIZE,
                        fill=cor_sombra,
                        outline=cor_ativa
                    )

        if self.game.game_over:
            self._status.config(text=f"Game Over! Score final: {self.game.score}")
        else:
            self._status.config(text=f"Score: {self.game.score}")

if __name__ == "__main__":
    app = TetrisApp()
    app.mainloop()

