from pathlib import Path
import pygame

pygame.init()

# Paths
PATH_ROOT = Path(__file__).parents[0]
PATH_SPRITES = PATH_ROOT / "assets" / "sprites"
PATH_FONTS = PATH_ROOT / "assets" / "fonts"

# Window Configuration
D_WIDTH = 1380
D_HEIGHT = 768
ROOT_DISPLAY = pygame.display.set_mode((D_WIDTH, D_HEIGHT))

# Main Clock
TICK_RATE = 60
GAME_CLOCK = pygame.time.Clock()

# Colors 
CLR_BACKGROUND = (209, 219, 228) # #d1dbe4

# Fonts
FONT_MAIN = pygame.font.Font(PATH_FONTS / 'silkscreen.ttf', 64)
FONT_UI = pygame.font.Font(PATH_FONTS / 'silkscreen.ttf', 32)

# Sprites
SPRT_MARBLE = pygame.image.load(PATH_SPRITES / "marble.png")
SPRT_BOARD = pygame.image.load(PATH_SPRITES / "board.png")
SPRT_BOARD = pygame.transform.scale(SPRT_BOARD, (650, 650))
SPRT_POSSIBLE_MOVE = pygame.image.load(PATH_SPRITES / "possible_ring.png")
SPRT_SELECTED_MARBLE = pygame.image.load(PATH_SPRITES / "select_ring.png")
