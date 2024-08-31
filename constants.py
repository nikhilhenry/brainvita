from collections import namedtuple
from pathlib import Path
import pygame

from utils import Position

pygame.init()

# Paths
PATH_ROOT = Path(__file__).parents[0]
PATH_SPRITES = PATH_ROOT / "assets" / "sprites"
PATH_FONTS = PATH_ROOT / "assets" / "fonts"
PATH_AUDIO = PATH_ROOT / "assets" / "audio"

# Window Configuration
D_WIDTH = 1380
D_HEIGHT = 768
ROOT_DISPLAY = pygame.display.set_mode((D_WIDTH, D_HEIGHT))


# Main Clock
TICK_RATE = 60
GAME_CLOCK = pygame.time.Clock()

# Colors
CLR_BACKGROUND = (209, 219, 228)  # #d1dbe4

# Fonts
FONT_MAIN = pygame.font.Font(PATH_FONTS / "silkscreen.ttf", 64)
FONT_UI = pygame.font.Font(PATH_FONTS / "silkscreen.ttf", 32)
FONT_UI_MONO = pygame.font.Font(PATH_FONTS / "synchronizer_nbp.ttf", 24)

# Sprites
SCALE_FACTOR = 3
SPRT_MARBLE = pygame.image.load(PATH_SPRITES / "marble1.png")  # 18x18
SPRT_MARBLE = pygame.transform.scale(
    SPRT_MARBLE, (18 * SCALE_FACTOR, 18 * SCALE_FACTOR)
)  # Scaling factor 3
SPRT_MARBLE_WIN = pygame.image.load(PATH_SPRITES / "marble2.png")  # 18x18
SPRT_MARBLE_WIN = pygame.transform.scale(
    SPRT_MARBLE_WIN, (18 * SCALE_FACTOR, 18 * SCALE_FACTOR)
)  # Scaling factor 3
SPRT_BOARD = pygame.image.load(PATH_SPRITES / "board.png")  # 198x198
SPRT_BOARD = pygame.transform.scale(
    SPRT_BOARD, (198 * SCALE_FACTOR, 198 * SCALE_FACTOR)
)  # Scaling factor 3
SPRT_POSSIBLE_MOVE = pygame.image.load(PATH_SPRITES / "possible_ring.png")
SPRT_POSSIBLE_MOVE = pygame.transform.scale(
    SPRT_POSSIBLE_MOVE, (18 * SCALE_FACTOR, 18 * SCALE_FACTOR)
)  # Scaling factor 3
SPRT_SELECTED_MARBLE = pygame.image.load(PATH_SPRITES / "select_ring.png")
SPRT_SELECTED_MARBLE = pygame.transform.scale(
    SPRT_SELECTED_MARBLE, (18 * SCALE_FACTOR, 18 * SCALE_FACTOR)
)  # scaling factor 3

# Buttons
SPRT_BFS_BTN = pygame.image.load(PATH_SPRITES / "bfs_button1.png")
SPRT_BFS_BTN_CLICKED = pygame.image.load(PATH_SPRITES / "bfs_button2.png")

SPRT_DFS_BTN = pygame.image.load(PATH_SPRITES / "dfs_button1.png")
SPRT_DFS_BTN_CLICKED = pygame.image.load(PATH_SPRITES / "dfs_button2.png")

SPRT_BESTFS_BTN = pygame.image.load(PATH_SPRITES / "bst_button1.png")
SPRT_BESTFS_BTN_CLICKED = pygame.image.load(PATH_SPRITES / "bst_button2.png")

SPRT_MUSIC_OFF_BTN_HOVERED = pygame.image.load(PATH_SPRITES / "music_bg4.png")
SPRT_MUSIC_OFF_BTN = pygame.image.load(PATH_SPRITES / "music_bg3.png")
SPRT_MUSIC_ON_BTN_HOVERED = pygame.image.load(PATH_SPRITES / "music_bg2.png")
SPRT_MUSIC_ON_BTN = pygame.image.load(PATH_SPRITES / "music_bg1.png")

SPRT_RESTART_BTN = pygame.image.load(PATH_SPRITES / "reset1.png")
SPRT_RESTART_BTN_CLICKED = pygame.image.load(PATH_SPRITES / "reset2.png")

SPRT_UNDO_BTN = pygame.image.load(PATH_SPRITES / "undo1.png")
SPRT_UNDO_BTN_CLICKED = pygame.image.load(PATH_SPRITES / "undo2.png")

# Sounds
SND_BG = pygame.mixer.Sound(str(PATH_AUDIO / "soundtrack.ogg"))
SND_MOVE = pygame.mixer.Sound(str(PATH_AUDIO / "marble1.ogg"))
SND_SELECT = pygame.mixer.Sound(str(PATH_AUDIO / "cut_select.ogg"))

# Set Display Properties
pygame.display.set_caption("Brainvita")
pygame.display.set_icon(SPRT_MARBLE)

# Game Constants

# Mapping of board position to coordinates
Coordinate = namedtuple("Coordinate", ["x", "y"])

POS2COORD = {}
for i in range(7):
    for j in range(7):
        # 198x198 board, 18x18 marbles, 36x36 is the padding before grid starts, no padding in between marbles
        POS2COORD[Position(i, j)] = Coordinate(
            ((D_WIDTH // 2) - (198 * SCALE_FACTOR // 2))
            + (36 * SCALE_FACTOR)
            + (j * 18 * SCALE_FACTOR),
            ((D_HEIGHT // 2) - (198 * SCALE_FACTOR // 2))
            + (36 * SCALE_FACTOR)
            + (i * 18 * SCALE_FACTOR),
        )
