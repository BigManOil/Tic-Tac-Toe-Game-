import pygame
import sys
import random
from typing import List, Tuple, Optional

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700
BOARD_SIZE = 3
CELL_SIZE = WIDTH // BOARD_SIZE
LINE_WIDTH = 15
CIRCLE_WIDTH = 15
CROSS_WIDTH = 20
CIRCLE_RADIUS = CELL_SIZE // 3
SPACE = CELL_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

# Font
font = pygame.font.Font(None, 40)

class GameStats:
    def __init__(self):
        self.stats = {'X': 0, 'O': 0, 'Tie': 0}

    def update(self, result):
        self.stats[result] += 1

class TicTacToe:
    def __init__(self, game_stats):
        self.board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.ai_difficulty = 'medium'
        self.game_stats = game_stats

    def make_move(self, row: int, col: int) -> bool:
        if self.board[row][col] == '' and not self.game_over:
            self.board[row][col] = self.current_player
            self.check_winner()
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self) -> None:
        # Check rows, columns and diagonals
        for i in range(BOARD_SIZE):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                self.winner = self.board[i][0]
                self.game_over = True
                return
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                self.winner = self.board[0][i]
                self.game_over = True
                return
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            self.winner = self.board[0][0]
            self.game_over = True
            return
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            self.winner = self.board[0][2]
            self.game_over = True
            return
        if all(self.board[i][j] != '' for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)):
            self.game_over = True
            self.winner = 'Tie'

    def ai_move(self) -> None:
        if self.ai_difficulty == 'easy':
            self.make_random_move()
        elif self.ai_difficulty == 'medium':
            if random.random() < 0.7:
                self.make_best_move()
            else:
                self.make_random_move()
        else:  # Hard
            self.make_best_move()

    def make_random_move(self) -> None:
        empty_cells = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if self.board[i][j] == '']
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.make_move(row, col)

    def make_best_move(self) -> None:
        best_score = float('-inf')
        best_move = None
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == '':
                    self.board[i][j] = 'O'
                    score = self.minimax(0, False)
                    self.board[i][j] = ''
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        if best_move:
            self.make_move(*best_move)

    def minimax(self, depth: int, is_maximizing: bool) -> int:
        if self.winner == 'O':
            return 1
        if self.winner == 'X':
            return -1
        if self.winner == 'Tie':
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if self.board[i][j] == '':
                        self.board[i][j] = 'O'
                        self.check_winner()
                        score = self.minimax(depth + 1, False)
                        self.board[i][j] = ''
                        self.winner = None
                        self.game_over = False
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if self.board[i][j] == '':
                        self.board[i][j] = 'X'
                        self.check_winner()
                        score = self.minimax(depth + 1, True)
                        self.board[i][j] = ''
                        self.winner = None
                        self.game_over = False
                        best_score = min(score, best_score)
            return best_score

    def reset(self) -> None:
        self.board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None

def draw_lines() -> None:
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, CELL_SIZE), (WIDTH, CELL_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * CELL_SIZE), (WIDTH, 2 * CELL_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE, 0), (CELL_SIZE, WIDTH), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * CELL_SIZE, 0), (2 * CELL_SIZE, WIDTH), LINE_WIDTH)

def draw_figures(board: List[List[str]]) -> None:
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * CELL_SIZE + CELL_SIZE // 2), int(row * CELL_SIZE + CELL_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * CELL_SIZE + SPACE, row * CELL_SIZE + CELL_SIZE - SPACE), (col * CELL_SIZE + CELL_SIZE - SPACE, row * CELL_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * CELL_SIZE + SPACE, row * CELL_SIZE + SPACE), (col * CELL_SIZE + CELL_SIZE - SPACE, row * CELL_SIZE + CELL_SIZE - SPACE), CROSS_WIDTH)

def draw_status(game: TicTacToe) -> None:
    if game.game_over:
        if game.winner == 'Tie':
            message = "It's a Tie!"
        else:
            message = f"Player {game.winner} wins!"
        text = font.render(message, True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 60))
    else:
        message = f"Player {game.current_player}'s turn"
        text = font.render(message, True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 60))

def draw_stats(stats: dict) -> None:
    text = font.render(f"X: {stats['X']}  O: {stats['O']}  Ties: {stats['Tie']}", True, (255, 255, 255))
    screen.blit(text, (10, HEIGHT - 110))

def draw_difficulty(difficulty: str) -> None:
    text = font.render(f"AI: {difficulty.capitalize()}", True, (255, 255, 255))
    screen.blit(text, (WIDTH - text.get_width() - 10, HEIGHT - 110))

def main() -> None:
    game_stats = GameStats()
    game = TicTacToe(game_stats)
    clock = pygame.time.Clock()
    game_result_processed = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
                mouseX = event.pos[0] // CELL_SIZE
                mouseY = event.pos[1] // CELL_SIZE
                if mouseY < BOARD_SIZE:  # Ensure click is within the board
                    if game.make_move(mouseY, mouseX):
                        if not game.game_over:
                            game.ai_move()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                    game_result_processed = False
                elif event.key == pygame.K_e:
                    game.ai_difficulty = 'easy'
                elif event.key == pygame.K_m:
                    game.ai_difficulty = 'medium'
                elif event.key == pygame.K_h:
                    game.ai_difficulty = 'hard'

        screen.fill(BG_COLOR)
        draw_lines()
        draw_figures(game.board)
        draw_status(game)
        draw_stats(game.game_stats.stats)
        draw_difficulty(game.ai_difficulty)

        if game.game_over and not game_result_processed:
            if game.winner != 'Tie':
                game.game_stats.update(game.winner)
            else:
                game.game_stats.update('Tie')
            game_result_processed = True

        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()