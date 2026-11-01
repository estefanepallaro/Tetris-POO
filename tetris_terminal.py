# Interface de terminal

from tetris import Tetris

def colored_board(game: Tetris) -> str:
    board = []
    for row in range(game.height):
        row_str = []
        for col in range(game.width):
            color = game.color_at(col, row)
            if color is None:
                row_str.append("⬛")
            else:
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)
                row_str.append(f"\033[38;2;{r};{g};{b}m██\033[0m")
        board.append(''.join(row_str))
    return '\n'.join(board)

def main() -> None:
    game = Tetris()
    while not game.game_over:
        print(colored_board(game))
        comando = input("Digite (a: esquerda, d: direita, s: baixo, w: girar, x: cair, q: sair): ")
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