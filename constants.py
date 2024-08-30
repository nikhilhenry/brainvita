from pathlib import Path
import pygame

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
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

# Sprites
SCALE_FACTOR = 3
SPRT_MARBLE = pygame.image.load(PATH_SPRITES / "marble.png")  # 18x18
SPRT_MARBLE = pygame.transform.scale(
    SPRT_MARBLE, (18 * SCALE_FACTOR, 18 * SCALE_FACTOR)
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
SPRT_BTN = pygame.image.load(PATH_SPRITES / "temp_buttonNormal.png")
SPRT_BTN_HOVERED = pygame.image.load(PATH_SPRITES / "temp_buttonHover.png")
SPRT_BTN_CLICKED = pygame.image.load(PATH_SPRITES / "temp_buttonPressed.png")

# Sounds
SND_BG = pygame.mixer.Sound(str(PATH_AUDIO / "soundtrack.ogg"))
SND_MOVE = pygame.mixer.Sound(str(PATH_AUDIO / "marble1.ogg"))
SND_SELECT = pygame.mixer.Sound(str(PATH_AUDIO / "cut_select.ogg"))

# Set Display Properties
pygame.display.set_caption('Brainvita')
pygame.display.set_icon(SPRT_MARBLE)
