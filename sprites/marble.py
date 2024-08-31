import pygame

from board import NodeState
from constants import POS2COORD, SPRT_MARBLE
from utils import Position


class Marble(pygame.sprite.Sprite):
    def __init__(self, pos: Position, state: NodeState):
        super().__init__()

        self.image = SPRT_MARBLE
        self.rect = self.image.get_rect()

        self.pos = pos
        self.state = state

        # initial rect location
        if self.state == NodeState.FILLED:
            self.rect.x = POS2COORD[self.pos].x
            self.rect.y = POS2COORD[self.pos].y
        else:
            self.rect.x = -100
            self.rect.y = -100

    def update(self, new_pos: Position, state: NodeState) -> None:
        self.state = state
        if self.state == NodeState.FILLED:
            self.pos = new_pos
            self.rect.x = POS2COORD[self.pos].x
            self.rect.y = POS2COORD[self.pos].y
        else:
            self.rect.x = -100
            self.rect.y = -100
