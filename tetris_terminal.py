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
    R = "\033[38;2;240;0;0m"
    L = "\033[38;2;240;160;0m"
    A = "\033[38;2;240;240;0m"
    V = "\033[38;2;0;240;0m"
    C = "\033[38;2;0;240;240m"
    P = "\033[38;2;160;0;240m"
    Z = "\033[0m"  # Reset

    letreiro_colorido = (
        f"{R}  _______ {L}     {A} _   {V}     {C} _ {P}    {Z}\n"
        f"{R} |__   __|{L}     {A}| |  {V}     {C}(_){P}    {Z}\n"
        f"{R}    | |   {L} ___ {A}| |_ {V}_ __ {C} _ {P}___ {Z}\n"
        f"{R}    | |   {L}/ _ \\{A}| __|{V} '__|{C}| |{P}/ __|{Z}\n"
        f"{R}    | |  {L}|  __/{A}| |_ {V}| |  {C}| |{P}\\__ \\{Z}\n"
        f"{R}    |_|   {L}\\___|{A} \\__|{V}|_|  {C}|_|{P}|___/{Z}\n"
    )
    print(letreiro_colorido)

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