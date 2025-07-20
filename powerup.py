import math

from circleshape import CircleShape
from random import uniform
import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, POWERUP_RADIUS, SPEED_MIN_SPEED, SPEED_VEL


class Powerup(CircleShape):
    def __init__(self, type, color=(0, 0, 255)):
        x = uniform(25, SCREEN_WIDTH - 25)
        y = uniform(25, SCREEN_HEIGHT - 25)

        self.color = color
        self.type = type
        self.speed = SPEED_MIN_SPEED

        if self.type == "speed":
            radius = POWERUP_RADIUS * 5
        else:
            radius = POWERUP_RADIUS

        super().__init__(x, y, radius=radius)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.position.x, self.position.y), self.radius, width=2)

    def move(self, player, dt):
        # Calculate direction vector from powerup to player
        direction = pygame.Vector2(
            player.position.x - self.position.x,
            player.position.y - self.position.y
        )

        # Normalize the direction vector (make it length 1)
        if direction.length() > 0:  # Avoid division by zero
            direction = direction.normalize()

        # Move in that direction
        self.position += direction * self.speed * dt

        self.speed += SPEED_VEL

    def reset(self):
        self.position.x = uniform(25, SCREEN_WIDTH - 25)
        self.position.y = uniform(25, SCREEN_HEIGHT - 25)

        self.speed = SPEED_MIN_SPEED