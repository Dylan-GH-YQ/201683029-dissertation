import pygame
import sys
from pygame.locals import *

class GobangGame:
    def __init__(self, sock=None, player=None, color='black'):
        # Pygame Initialization
        pygame.init()

        # Game variables
        self.screen = pygame.display.set_mode((760, 560))
        pygame.display.set_caption("Gobang")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.SADDLEBROWN = (139, 69, 19)
        self.DARKBROWN = (101, 67, 33)
        self.LIGHTGRAY = (200, 200, 200)

        # Fonts
        self.font = pygame.font.SysFont("Arial", 20)
        self.big_font = pygame.font.SysFont("Arial", 25)

        # Game board
        self.GRID_SIZE = 35
        self.BOARD_SIZE = 15
        self.PIECE_SIZE = 10
        self.MARGIN_X, self.MARGIN_Y = 32, 38
        self.UI_WIDTH = 140

        self.click_x, self.click_y = 0, 0
        self.pieces_x = [i for i in range(self.MARGIN_X, self.MARGIN_X + self.GRID_SIZE * self.BOARD_SIZE, self.GRID_SIZE)]
        self.pieces_y = [i for i in range(self.MARGIN_Y, self.MARGIN_Y + self.GRID_SIZE * self.BOARD_SIZE, self.GRID_SIZE)]
        self.person_flag = 1
        self.piece_color = color
        self.game_over = False
        self.sock = sock
        self.player = player
        self.coor_black = []
        self.coor_white = []

        # Load images
        self.background_image = pygame.image.load("background.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.GRID_SIZE * (self.BOARD_SIZE - 1), self.GRID_SIZE * (self.BOARD_SIZE - 1)))
        self.black_piece = pygame.image.load("black_stone.png")
        self.black_piece = pygame.transform.scale(self.black_piece, (self.GRID_SIZE, self.GRID_SIZE))
        self.white_piece = pygame.image.load("white_stone.png")
        self.white_piece = pygame.transform.scale(self.white_piece, (self.GRID_SIZE, self.GRID_SIZE))

    def draw_board(self):
        self.screen.fill(self.SADDLEBROWN)
        self.screen.blit(self.background_image, (self.MARGIN_X, self.MARGIN_Y))
        for i in range(self.BOARD_SIZE):
            pygame.draw.line(self.screen, self.BLACK, (self.MARGIN_X, self.MARGIN_Y + i * self.GRID_SIZE), (self.MARGIN_X + (self.BOARD_SIZE - 1) * self.GRID_SIZE, self.MARGIN_Y + i * self.GRID_SIZE))
            pygame.draw.line(self.screen, self.BLACK, (self.MARGIN_X + i * self.GRID_SIZE, self.MARGIN_Y), (self.MARGIN_X + i * self.GRID_SIZE, self.MARGIN_Y + (self.BOARD_SIZE - 1) * self.GRID_SIZE))

        for point in [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7)]:
            pygame.draw.circle(self.screen, self.BLACK, (self.MARGIN_X + point[0] * self.GRID_SIZE, self.MARGIN_Y + point[1] * self.GRID_SIZE), 5)

        # Draw numeric coordinates
        for i in range(self.BOARD_SIZE):
            label = self.font.render(str(i + 1), True, self.BLACK)
            self.screen.blit(label, (self.MARGIN_X - 20, self.MARGIN_Y + i * self.GRID_SIZE - 10))

        # Draw letter coordinates
        for i in range(self.BOARD_SIZE):
            label = self.font.render(chr(65 + i), True, self.BLACK)
            self.screen.blit(label, (self.MARGIN_X + i * self.GRID_SIZE - 5, self.MARGIN_Y - 30))

    def count_pieces(self, coor, pieces_count, t1, t2):
        for i in range(1, 5):
            x, y = self.click_x + t1 * self.GRID_SIZE * i, self.click_y + t2 * self.GRID_SIZE * i
            if (x, y) in coor:
                pieces_count += 1
            else:
                break
        return pieces_count

    def pre_judge(self, piece_color):
        if piece_color == "black":
            self.real_judge(self.coor_black)
        elif piece_color == "white":
            self.real_judge(self.coor_white)

    def real_judge(self, coor):
        if self.real_judge_1(coor) == 1 or self.real_judge_2(coor) == 1:
            self.game_over = True

    def real_judge_1(self, coor):
        pieces_count = 0
        pieces_count = self.count_pieces(coor, pieces_count, 1, 0)
        pieces_count = self.count_pieces(coor, pieces_count, -1, 0)
        if pieces_count >= 4:
            return 1
        else:
            pieces_count = 0
            pieces_count = self.count_pieces(coor, pieces_count, 0, -1)
            pieces_count = self.count_pieces(coor, pieces_count, 0, 1)
            if pieces_count >= 4:
                return 1
            else:
                return 0

    def real_judge_2(self, coor):
        pieces_count = 0
        pieces_count = self.count_pieces(coor, pieces_count, 1, 1)
        pieces_count = self.count_pieces(coor, pieces_count, -1, -1)
        if pieces_count >= 4:
            return 1
        else:
            pieces_count = 0
            pieces_count = self.count_pieces(coor, pieces_count, 1, -1)
            pieces_count = self.count_pieces(coor, pieces_count, -1, 1)
            if pieces_count >= 4:
                return 1
            else:
                return 0

    def put_piece(self, piece_color):
        if piece_color == "white":
            self.coor_white.append((self.click_x, self.click_y))
        elif piece_color == "black":
            self.coor_black.append((self.click_x, self.click_y))
        self.pre_judge(piece_color)

    def coor_judge(self):
        coor = self.coor_black + self.coor_white
        item = None
        min_dist = float('inf')
        for x in self.pieces_x:
            for y in self.pieces_y:
                dist = (self.click_x - x) ** 2 + (self.click_y - y) ** 2
                if dist < min_dist:
                    min_dist = dist
                    item = (x, y)
        if item:
            self.click_x, self.click_y = item
            if (self.click_x, self.click_y) not in coor:
                if self.person_flag != 0:
                    if self.person_flag == 1:
                        self.put_piece("black")
                        self.piece_color = "white"
                        self.person_flag = -1
                    elif self.person_flag == -1:
                        self.put_piece("white")
                        self.piece_color = "black"
                        self.person_flag = 1

    def game_reset(self):
        self.person_flag = 1
        self.piece_color = "black"
        self.coor_black = []
        self.coor_white = []
        self.game_over = False

    def draw_reset_button(self):
        reset_x = 580
        reset_y = 430
        reset_width = self.UI_WIDTH - 10
        reset_height = 40
        reset_surface = pygame.Surface((reset_width, reset_height), pygame.SRCALPHA)
        reset_surface.fill((255, 255, 255, 0))
        reset_text = self.big_font.render("Restart", True, self.BLACK)
        text_rect = reset_text.get_rect(center=(reset_width // 2, reset_height // 2))
        reset_surface.blit(reset_text, text_rect)
        self.screen.blit(reset_surface, (reset_x, reset_y))
        return pygame.Rect(reset_x, reset_y, reset_width, reset_height)

    def draw_piece_hint(self):
        hint_x = 580
        hint_y = 60
        hint_surface = pygame.Surface((self.UI_WIDTH - 10, 60), pygame.SRCALPHA)
        hint_surface.fill((255, 255, 255, 0))
        hint_text = self.big_font.render(f"It's {'Black Turn' if self.piece_color == 'black' else 'White Turn'}", True, self.BLACK)
        hint_surface.blit(hint_text, (0, 0))
        self.screen.blit(hint_surface, (hint_x, hint_y))

    def show_game_over_dialog(self):
        dialog_width = 300
        dialog_height = 200
        dialog_x = (760 - dialog_width) // 2
        dialog_y = (560 - dialog_height) // 2

        dialog_surface = pygame.Surface((dialog_width, dialog_height))
        dialog_surface.fill(self.DARKBROWN)

        result_text = self.big_font.render("Game Over", True, self.WHITE)
        win_text = self.big_font.render("Black Win" if self.person_flag == -1 else "White Win", True, self.WHITE)

        confirm_button = pygame.Rect((dialog_width - 100) // 2, dialog_height - 60, 100, 40)
        pygame.draw.rect(dialog_surface, self.SADDLEBROWN, confirm_button)
        pygame.draw.rect(dialog_surface, self.BLACK, confirm_button, 2)
        confirm_text = self.font.render("Confirm", True, self.WHITE)
        confirm_text_rect = confirm_text.get_rect(center=confirm_button.center)

        dialog_surface.blit(result_text, (90, 30))
        dialog_surface.blit(win_text, (90, 80))
        dialog_surface.blit(confirm_text, confirm_text_rect)

        self.screen.blit(dialog_surface, (dialog_x, dialog_y))
        pygame.display.flip()

        waiting_for_confirm = True
        while waiting_for_confirm:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    mx -= dialog_x
                    my -= dialog_y
                    if confirm_button.collidepoint(mx, my):
                        self.game_reset()
                        waiting_for_confirm = False

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            self.screen.fill(self.SADDLEBROWN)
            self.draw_board()
            reset_button = self.draw_reset_button()
            self.draw_piece_hint()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if reset_button.collidepoint(event.pos):
                        self.game_reset()
                    elif not self.game_over:
                        self.click_x, self.click_y = event.pos
                        self.coor_judge()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.game_reset()

            for pos in self.coor_black:
                self.screen.blit(self.black_piece, (pos[0] - self.GRID_SIZE // 2, pos[1] - self.GRID_SIZE // 2))
            for pos in self.coor_white:
                self.screen.blit(self.white_piece, (pos[0] - self.GRID_SIZE // 2, pos[1] - self.GRID_SIZE // 2))

            if self.game_over:
                self.show_game_over_dialog()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GobangGame()
    game.run()
