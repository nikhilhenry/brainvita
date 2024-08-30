import pygame


class ImageButton:
    """
    Custom PyGame Image Button class. Written by @PjrCodes on GitHub.
    """

    def __init__(
        self,
        location: tuple[int, int],
        default_surface: pygame.Surface,
        hovered_surface: pygame.Surface | None = None,
        clicked_surface: pygame.Surface | None = None,
    ):
        # button state
        self.is_clicked = False

        self.scr_location = location
        self.default_surface = default_surface

        self.width = self.default_surface.get_width()
        self.height = self.default_surface.get_height()

        self.top_border = self.scr_location[1]  # Y of top left of rect
        self.right_border = (
            self.scr_location[0] + self.width
        )  # X of top left of rect plus width
        self.bottom_border = (
            self.scr_location[1] + self.height
        )  # Y of top left of rect plus height
        self.left_border = self.scr_location[0]  # X of top left of rect

        if hovered_surface is None:
            self.hovered_surface = self.default_surface
        else:
            self.hovered_surface = hovered_surface

        if clicked_surface is None:
            self.clicked_surface = self.default_surface
        else:
            self.clicked_surface = clicked_surface

    @property
    def hovered(self):
        """Return a boolean representing if mouse is hovering over button."""
        if self.default_surface.get_rect().collidepoint(pygame.mouse.get_pos()):
            return True
        else:
            return False

    def draw(self, surface: pygame.Surface):
        """Draw the button on the screen. The button draws at the location specified in the constructor."""
        if self.is_clicked:
            # if the button is clicked, draw the clicked surface. We can only be clicked if we are hovered
            surface.blit(self.clicked_surface, self.scr_location)
        elif self.hovered:
            # if the button is hovered (but not clicked), draw the hovered surface
            surface.blit(self.hovered_surface, self.scr_location)
        else:
            surface.blit(self.default_surface, self.scr_location)
