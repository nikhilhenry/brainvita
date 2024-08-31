from typing import Any, Callable
import pygame


class ImageButton(pygame.sprite.Sprite):
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
        super().__init__()
        # button state
        self.is_clicked = False

        self.x, self.y = location
        self.default_surface = default_surface

        if hovered_surface is None:
            self.hovered_surface = self.default_surface
        else:
            self.hovered_surface = hovered_surface

        if clicked_surface is None:
            self.clicked_surface = self.default_surface
        else:
            self.clicked_surface = clicked_surface

        self.image = self.default_surface
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    @property
    def hovered(self) -> bool:
        """Return a boolean representing if mouse is hovering over button."""
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        else:
            return False

    def update(self) -> None:
        """Update button state."""
        if self.is_clicked:
            # if the button is clicked, draw the clicked surface. We can only be clicked if we are hovered
            self.image = self.clicked_surface
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            # surface.blit(self.clicked_surface, self.scr_location)
        elif self.hovered:
            # if the button is hovered (but not clicked), draw the hovered surface
            self.image = self.hovered_surface
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            # surface.blit(self.hovered_surface, self.scr_location)
        else:
            self.image = self.default_surface
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            # surface.blit(self.default_surface, self.scr_location)

    def reset(self) -> None:
        """Reset button state."""
        self.is_clicked = False
        self.image = self.default_surface
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def click(self) -> None:
        """Set button state to clicked."""
        self.is_clicked = True

    def unclick(self) -> None:
        """Set button state to unclicked."""
        self.is_clicked = False


class ImageToggleButton(pygame.sprite.Sprite):
    """
    Custom PyGame Image Toggle Button class. Written by @PjrCodes on GitHub.
    """

    def __init__(
        self,
        location: tuple[int, int],
        default_surface: pygame.Surface,
        toggled_surface: pygame.Surface,
        default_hovered_surface: pygame.Surface | None = None,
        toggled_hovered_surface: pygame.Surface | None = None,
    ):
        super().__init__()
        # button state
        self.is_toggled = False  # this is the same as is_toggled

        self.x, self.y = location
        self.default_surface = default_surface
        self.toggled_surface = toggled_surface

        if default_hovered_surface is None:
            self.default_hovered_surface = self.default_surface
        else:
            self.default_hovered_surface = default_hovered_surface

        if toggled_hovered_surface is None:
            self.toggled_hovered_surface = self.toggled_surface
        else:
            self.toggled_hovered_surface = toggled_hovered_surface

        self.image = self.default_surface
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    @property
    def hovered(self) -> bool:
        """Return a boolean representing if mouse is hovering over button."""
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        else:
            return False

    def update(self) -> None:
        """Update button state."""

        if self.hovered:
            if self.is_toggled:
                self.image = self.toggled_hovered_surface
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
            else:
                self.image = self.default_hovered_surface
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
        else:
            if self.is_toggled:
                self.image = self.toggled_surface
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
            else:
                self.image = self.default_surface
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y

    def reset(self) -> None:
        """Reset button state."""
        self.is_toggled = False
        self.image = self.default_surface
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def click(self) -> None:
        """Set button state to clicked."""
        self.is_toggled = not self.is_toggled
