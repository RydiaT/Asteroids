from circleshape import CircleShape
import pygame
from constants import ASTEROID_MIN_RADIUS
from random import uniform
from particle import create_cloud


class Asteroid(CircleShape):
    def __init__(self, x, y, radius, color=(255, 255, 255)):
        super().__init__(x, y, radius)

        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.position.x, self.position.y), self.radius, width=2)

    def update(self, dt):
        self.position += (self.velocity * dt)

    def split(self):
        create_cloud(self.position)
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        angle = uniform(20, 50)

        new_angle1 = self.velocity.rotate(angle)
        new_angle2 = self.velocity.rotate(-angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        new1 = Asteroid(self.position, self.position, new_radius, self.color)
        new1.velocity = new_angle1 * 1.2
        new2 = Asteroid(self.position, self.position, new_radius, self.color)
        new2.velocity = new_angle2 * 1.2