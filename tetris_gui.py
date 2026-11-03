import tkinter as tk

from tetris import Tetris
from collections.abc import Callable


class TetrisApp(tk.Tk):
    CELL_SIZE = 35

    # cores Game Boy
    COR_COLUNA = "#0b1b22"
    COR_CAIXA = "#dbe7b4"
    COR_BORDA = "#3d5a57"
    COR_TEXTO = "#10261d"

    def __init__(self):
        super().__init__()

        # configurações da janela

        self.title("Tetris")

        self.configure(bg = "black")

        # jogo
        self.game = Tetris()

        self._after_id: str | None = None

        self._paused = False

        self._easter_clicks = 0
        self._easter_after_id = None
        self._easter_text = ""
        self._easter_unlocked = False

        painel_titulo = tk.Frame(
            self,
            bg="black",
        )
        painel_titulo.pack(pady=10)

        letras_cores = [
            ("T", "#f00000"),  # vermelho
            ("E", "#f0a000"),  # laranja
            ("T", "#f0f000"),  # amarelo
            ("R", "#00f000"),  # verde
            ("I", "#00f0f0"),  # ciano
            ("S", "#a000f0"),  # roxo
        ]

        for letra, cor in letras_cores:
            lbl = tk.Label(
                painel_titulo,
                text=letra,
                font=("Arial", 36, "bold"),
                fg=cor,
                bg="black",
            )

            lbl.pack(side=tk.LEFT)

        # Estrutura do jogo

        carcaca = tk.Frame(
            self,
            bg="#d8d7d2",
            padx=35,
            pady=25,
            highlightthickness=2,
            highlightbackground="#b5b4b0",
        )

        carcaca.pack(pady=10)

        moldura_tela = tk.Frame(
            carcaca,
            bg="#6f6d78",
            padx=28,
            pady=18,
            highlightthickness=3,
            highlightbackground="#5a5866",
        )

        moldura_tela.pack()

        topo_tela = tk.Frame(
            moldura_tela,
            bg="#777584",
        )

        topo_tela.pack(
            fill="x",
            pady=(0, 8),
        )

        # Um ponto qualquer...
        apenas_ponto = tk.Button(
            topo_tela,
            text="●",
            bg="#777584",
            fg="#00ff00",
            activebackground="#777584",
            activeforeground="#00ff00",
            font=("Arial", 20),
            bd=0,
            relief="flat",
            highlightthickness=0,
            command=self._easter_egg,
        )

        apenas_ponto.pack(
            side=tk.LEFT,
            padx=0,
        )

        # Cabeçalho do jogo
        tk.Label(
            topo_tela,
            text=" UFOPA",
            bg="#777584",
            fg="#c9c7c9",
            font=("Arial", 10, "bold"),
        ).pack(
            side=tk.LEFT,
            padx=0,
        )

        tk.Label(
            topo_tela,
            text="Trabalho de POO",
            bg="#777584",
            fg="#c9c7c9",
            font=("Arial", 10, "bold"),
        ).pack(
            side=tk.RIGHT,
        )

        # Area do jogo
        area_jogo = tk.Frame(
            moldura_tela,
            bg="#777584",
        )

        area_jogo.pack(
            padx=8,
            pady=8,
        )

        self._canvas = tk.Canvas(
            area_jogo,
            width=self.game.width * self.CELL_SIZE,
            height=self.game.height * self.CELL_SIZE,
            bg="#9bbc0f",
            highlightthickness=4,
            highlightbackground="#32352a",
        )

        self._canvas.pack(
            side=tk.LEFT,
            padx=(0, 12),
        )

        # painel de informações do jogo

        painel_direito = tk.Frame(
            area_jogo,
            bg=self.COR_COLUNA,
            padx=10,
            pady=12,
        )

        painel_direito.pack(
            side=tk.LEFT,
            fill="y",
        )

        # SCORE, LEVEL, LINES
        self._score_label = self._caixa_gameboy(
            painel_direito,
            "SCORE",
            "000000",
        )

        self._level_label = self._caixa_gameboy(
            painel_direito,
            "LEVEL",
            "1",
        )

        self._lines_label = self._caixa_gameboy(
            painel_direito,
            "LINES",
            "0",
        )

        # Visualização da próxima peça

        preview_box = tk.Frame(
            painel_direito,
            bg=self.COR_CAIXA,
            highlightthickness=3,
            highlightbackground=self.COR_BORDA,
            padx=10,
            pady=10,
        )

        preview_box.pack(
            pady=12,
        )

        self._preview = tk.Canvas(
            preview_box,
            width=4 * self.CELL_SIZE,
            height=4 * self.CELL_SIZE,
            bg=self.COR_CAIXA,
            highlightthickness=0,
        )

        self._preview.pack()

        # Game Over

        self._game_over_box = tk.Frame(
            painel_direito,
            bg = self.COR_COLUNA,
        )

        self._game_over_box.pack(
            fill = "both",
            expand = True,
            pady = (12, 0)
        )

        self._game_over_label = tk.Label(
            self._game_over_box,
            text = "",
            bg = self.COR_COLUNA,
            fg = self.COR_CAIXA,
            font = ("Courier", 16, "bold"),
            justify = "center"
        )
        self._game_over_label.pack(
            expand = True
        )

        # Rodapé do jogo

        rodape = tk.Frame(
            carcaca,
            bg="#d8d7d2",
        )

        rodape.pack(
            fill ="x",
            pady=(8, 2),
        )

        tk.Label(
            rodape,
            text="EFRENDO",
            bg="#d8d7d2",
            fg="#343477",
            font=("Arial", 11, "bold"),
        ).pack(
            side=tk.LEFT,
        )

        tk.Label(
            rodape,
            text=" SYSTEM C",
            bg="#d8d7d2",
            fg="#343477",
            font=("Arial", 11, "bold"),
        ).pack(
            side=tk.LEFT,
        )

        # Botões de controle do jogo
        restart_button = tk.Button(
            rodape,
            text="Reiniciar",
            command = self._restart,
        )

        restart_button.pack(
            side = tk.RIGHT
        )

        self._pause_button = tk.Button(
            rodape,
            text = "Pausar",
            command = self._toggle_pause
        )

        self._pause_button.pack(
            side = tk.RIGHT,
            padx = (0, 6)
        )

        # Controles do teclado
        self.bind(
            "<Left>",
            lambda _: self._play(self.game.move_left),
        )

        self.bind(
            "<Right>",
            lambda _: self._play(self.game.move_right),
        )

        self.bind(
            "<Down>",
            lambda _: self._play(self.game.move_down),
        )

        self.bind(
            "<Up>",
            lambda _: self._play(self.game.rotate),
        )

        self.bind(
            "<space>",
            lambda _: self._play(self.game.drop),
        )

        self._draw()
        self._schedule_fall()

    # Funções auxiliares
    def _caixa_gameboy(
        self,
        parent,
        titulo: str,
        valor: str,
    ):
        caixa = tk.Frame(
            parent,
            bg=self.COR_CAIXA,
            highlightthickness=3,
            highlightbackground=self.COR_BORDA,
            padx=10,
            pady=8,
        )

        caixa.pack(
            pady=8,
            fill="x",
        )

        titulo_label = tk.Label(
            caixa,
            text=titulo,
            bg=self.COR_CAIXA,
            fg=self.COR_TEXTO,
            font=("Courier", 16, "bold"),
        )

        titulo_label.pack()

        valor_label = tk.Label(
            caixa,
            text=valor,
            bg=self.COR_CAIXA,
            fg=self.COR_TEXTO,
            font=("Courier", 20, "bold"),
        )

        valor_label.pack()

        return valor_label

    # Uma função qualquer...

    def _apenas_ponto(self):
        self._easter_clicks += 1

        if self._easter_after_id is not None:
            self.after_cancel(
                self._easter_after_id
            )

            self._easter_after_id = None

        if self._easter_clicks == 2:
            self._easter_text = "Olha o click!"

            self._draw()

            self._easter_after_id = self.after(
                2000,
                self._limpar_easter_text
            )

        elif self._easter_clicks == 5:
            self._easter_text = (
                "Python gosta de um\n"
                "underline!"
            )

            self._draw()

            self._easter_after_id = self.after(
                2500,
                self._limpar_easter_text
            )

        elif self._easter_clicks == 7:
            self._easter_text = (
                "ATARI 2600 REFERENCE\n\n"
                "DIREÇÃO\n"
                "Éfren Lopes de Souza\n\n"
                "CREATED BY\n\n"
                "Arthur Vinicius\n"
                "Estéfane Pallaro\n"
                "Gustavo Augusto\n"
                "Helena Vinhote\n\n"
                "Obrigado Professor!"
            )

            self._draw()

            self._easter_after_id = self.after(
                7000,
                self._finalizar_apenas_ponto
            )

            self._easter_clicks = 0

    def _limpar_easter_text(self):
        self._easter_text = ""
        self._easter_after_id = None
        self._draw()

    def _finalizar_apenas_ponto(self):
        self._easter_text = ""
        self._easter_after_id = None
        self._easter_unlocked = True

        self.game.easter_bonus()

        self._draw()

    # Play

    def _play(
        self,
        move: Callable[[], None],
    ):
        if self._paused:
            return
        
        move()
        self._draw()

    # Velocidade de queda do tetrimino

    def _schedule_fall(self):
        if self.game.score >= 10000000:
            velocidade = 100

        else:
            velocidade = 500 - (
                (self.game.level - 1) * 20
            )

            if velocidade < 200:
                velocidade = 200

        self._after_id = self.after(
            velocidade,
            self._fall
        )

    # Funções de desenho do jogo
    def _fall(self):
        if not self.game.game_over:

            if not self._paused:

                self.game.move_down()
                self._draw()
            self._schedule_fall()

    # Pausar
    def _toggle_pause(self):
        self._paused = not self._paused

        if self._paused:
            self._pause_button.config(
                text="Continuar"
            )
        else:
            self._pause_button.config(
                text="Pausar"
            )
    # Reiniciar
    def _restart(self):
        if self._after_id is not None:
            self.after_cancel(
                self._after_id
            )

        self._paused = False

        if self._easter_after_id is not None:
            self.after_cancel(
                self._easter_after_id
            )

        self._easter_clicks = 0
        self._easter_after_id = None
        self._easter_text = ""
        self._easter_unlocked = False

        self._pause_button.config(
            text="Pausar"
        )

        self.game.reset()
        self._draw()
        self._schedule_fall()

    # Desenho do jogo

    def _draw(self):
        self._canvas.delete("all")

        if not self.game.game_over:
            sombra = self.game.ghost_cells()
            cor_ativa = self.game.active_tetrimino.color

            r = int(
                int(cor_ativa[1:3], 16) * 0.3
                + 255 * 0.7
            )

            g = int(
                int(cor_ativa[3:5], 16) * 0.3
                + 255 * 0.7
            )

            b = int(
                int(cor_ativa[5:7], 16) * 0.3
                + 255 * 0.7
            )

            cor_sombra = (
                f"#{r:02x}{g:02x}{b:02x}"
            )

        else:
            sombra = set()
            cor_sombra = None
            cor_ativa = None

        for col in range(self.game.width):
            for row in range(self.game.height):
                color = self.game.color_at(
                    col,
                    row,
                )

                if color is not None:
                    # bloco normal
                    self._canvas.create_rectangle(
                        col * self.CELL_SIZE,
                        row * self.CELL_SIZE,
                        (col + 1) * self.CELL_SIZE,
                        (row + 1) * self.CELL_SIZE,
                        fill=color,
                        outline="black",
                    )

                elif (col, row) in sombra:
                    # sombra
                    self._canvas.create_rectangle(
                        col * self.CELL_SIZE,
                        row * self.CELL_SIZE,
                        (col + 1) * self.CELL_SIZE,
                        (row + 1) * self.CELL_SIZE,
                        fill=cor_sombra,
                        outline=cor_ativa,
                    )

        if self._easter_unlocked:
            self._score_label.config(
                text = str(self.game.score)
            )
        else:
            self._score_label.config(
                text = f"{self.game.score:06d}"
            )

        if self._easter_unlocked:
            self._level_label.config(
                text="Éfren"
            )
        else:
            self._level_label.config(
                text=str(self.game.level)
            )

        self._lines_label.config(
            text=str(self.game.lines)
        )

        self._draw_preview()

        if self._easter_text:
            self._game_over_label.config(
                text=self._easter_text
            )

        elif self.game.game_over:
            self._game_over_label.config(
                text=(
                    f"GAME OVER\n\n"
                    f"Score final\n"
                    f"{self.game.score}"
                )
            )

        else:
            self._game_over_label.config(
                text=""
            )
    # Desenho da próxima peça

    def _draw_preview(self):
        self._preview.delete("all")

        piece = self.game.next_tetrimino

        tamanho = 25

        largura = piece.box_size * tamanho
        altura = piece.box_size * tamanho

        canvas_largura = int(self._preview["width"])
        canvas_altura = int(self._preview["height"])

        offset_x = (canvas_largura - largura) // 2
        offset_y = (canvas_altura - altura) // 2

        for block in piece.shape:
            x1 = offset_x + block.x * tamanho
            y1 = offset_y + block.y * tamanho

            x2 = x1 + tamanho
            y2 = y1 + tamanho

            self._preview.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=piece.color,
                outline="#10261d",
            )
            
# Função principal
if __name__ == "__main__":
    app = TetrisApp()
    app.mainloop()