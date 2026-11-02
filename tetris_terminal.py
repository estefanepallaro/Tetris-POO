# Interface de terminal

from tetris import Tetris

def colored_board(game: Tetris) -> str:
    board = []

    active_cells = set(game._tetri_cells(game._tetri_col, game._tetri_row))
    ghost = game.ghost_cells()

    for row in range(game.height):
        row_str = []

        for col in range(game.width):
            color = game.color_at(col, row)

            if (col, row) in active_cells:
                color = game.active_tetrimino.color
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)

                row_str.append(f"\033[38;2;{r};{g};{b}m██\033[0m")

            elif (col, row) in ghost and color is None:
                color = game.active_tetrimino.color
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)

                row_str.append(f"\033[2;38;2;{r};{g};{b}m██\033[0m")

            elif color is None:
                row_str.append("  ")

            else:
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)

                row_str.append(f"\033[38;2;{r};{g};{b}m██\033[0m")

        board.append("".join(row_str))

    return "\n".join(board)

# letreiro no topo
def exibir_letreiro() -> None:
    RESET = "\033[0m"

    cores = [
        "\033[38;2;245;50;55m",    # T - vermelho
        "\033[38;2;255;190;15m",   # E - laranja
        "\033[38;2;255;225;90m",   # T - amarelo
        "\033[38;2;75;215;125m",   # R - verde
        "\033[38;2;70;145;240m",   # I - azul
        "\033[38;2;185;90;200m",   # S - roxo
    ]

    letras = {
    "T": [
        "111",
        "010",
        "010",
        "010",
        "010",
    ],

    "E": [
        "111",
        "100",
        "110",
        "100",
        "111",
    ],

    "R": [
        "110",
        "101",
        "110",
        "101",
        "101",
    ],

    "I": [
        "111",
        "010",
        "010",
        "010",
        "111",
    ],

    "S": [
        "111",
        "100",
        "111",
        "001",
        "111",
    ],
}

    palavra = "TETRIS"

    altura = 6
    largura_letra = 4

    # local que vai ser alocada as letras
    canvas = {}

    x_inicio = 0

    for indice, letra in enumerate(palavra):
        desenho = letras[letra]
        cor = cores[indice]

        for y, linha in enumerate(desenho):
            for x, pixel in enumerate(linha):

                if pixel == "1":


                    canvas[(x_inicio + x, y)] = ("██", cor)

        x_inicio += largura_letra

    for y in range(altura):
        linha = ""

        for x in range(x_inicio):
            if (x, y) in canvas:
                bloco, cor = canvas[(x, y)]
                linha += cor + bloco + RESET

            else:
                linha += "  "

        print(linha)


def bordas(game: Tetris):

    print("\033[2J\033[H", end="")
    exibir_letreiro()

    largura = game.width * 2

    linhas_tabuleiro = []
    linhas_tabuleiro.append("╔" + "=" * largura + "╗")

    for linha in colored_board(game).split("\n"):
        linhas_tabuleiro.append("║" + linha + "║")

    linhas_tabuleiro.append("╚" + "=" * largura + "╝")

    

    painel = [
        f"Score: {game.score}",
        "",
        "A - esquerda",
        "D - direita",
        "S - descer",
        "W - girar",
        "X - queda",
        "Q - sair",
    ]

    total_linhas = max(len(linhas_tabuleiro), len(painel))

    while len(linhas_tabuleiro) < total_linhas:
        linhas_tabuleiro.append(" " * (largura + 2))

    while len(painel) < total_linhas:
        painel.append("")

    for esquerda, direita in zip(linhas_tabuleiro, painel):
        print(f"{esquerda}   {direita}")

def main() -> None:
    game = Tetris()

    while not game.game_over:
        bordas(game)

        comando = input("> ").lower()

        match comando:
            case 'a':
                game.move_left()
            case 'd':
                game.move_right()
            case 's':
                game.move_down()
            case 'w':
                game.rotate()
            case 'x':
                game.drop()
            case 'q':
                break
    if game.game_over:
        print("Game Over!")

if __name__== '__main__':
    main()