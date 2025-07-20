import pygame
from circleshape import CircleShape
from random import uniform
from constants import PARTICLE_RADIUS, PARTICLE_COUNT


def create_cloud(position, color=(255, 255, 0)):
    # Create explosion particles
    for _ in range(PARTICLE_COUNT):
        particle = Particle(position.x, position.y, color)
        # Random velocity direction
        angle = uniform(0, 360)
        speed = uniform(100, 200)
        particle.velocity = pygame.Vector2(1, 0).rotate(angle) * speed


class Particle(CircleShape):
    def __init__(self, x, y, rgb_color=(255, 255, 0)):
        super().__init__(x, y, PARTICLE_RADIUS)  # Small radius for particles
        self.alpha = 255  # Start fully opaque
        self.fade_speed = uniform(100, 200)  # Random fade speed
        self.rgb_color = rgb_color
        self.rgb_color = rgb_color

    def draw(self, screen):
        # Create a surface with per-pixel alpha
        particle_surface = pygame.Surface((self.radius * 2 + 1, self.radius * 2 + 1), pygame.SRCALPHA)
        # Draw yellow circle with current alpha

        color = (self.rgb_color[0], self.rgb_color[1], self.rgb_color[2], self.alpha)

        pygame.draw.circle(particle_surface, color,
                         (self.radius + 1, self.radius + 1), self.radius)
        # Blit the particle surface onto the screen
        screen.blit(particle_surface,
                   (self.position.x - self.radius, self.position.y - self.radius))

    def update(self, dt):
        # Move particle
        self.position += (self.velocity * dt)
        # Reduce alpha
        self.alpha = max(0, self.alpha - self.fade_speed * dt)
        # Kill particle when fully transparent
        if self.alpha <= 0:
            self.kill()
