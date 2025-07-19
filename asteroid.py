from circleshape import CircleShape
import pygame
from constants import ASTEROID_MIN_RADIUS
from random import uniform


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.position.x, self.position.y), self.radius, width=2)

    def update(self, dt):
        self.position += (self.velocity * dt)

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        angle = uniform(20, 50)

        new_angle1 = self.velocity.rotate(angle)
        new_angle2 = self.velocity.rotate(-angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        new1 = Asteroid(self.position, self.position, new_radius)
        new1.velocity = new_angle1 * 1.2
        new2 = Asteroid(self.position, self.position, new_radius)
        new2.velocity = new_angle2 * 1.2