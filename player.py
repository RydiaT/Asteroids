from circleshape import CircleShape
from shot import Shot
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_MOVE_SPEED, PLAYER_SHOOT_SPEED, SHOT_COOLDOWN
import pygame
from particle import create_cloud


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0

        self.shot_timer = 0

        self.dying = False

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        if not self.dying:
            pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        start = pygame.Vector2(0, 1)
        start = start.rotate(self.rotation)

        start *= PLAYER_MOVE_SPEED * dt

        self.position += start

    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity *= PLAYER_SHOOT_SPEED

    def game_over(self):
        create_cloud(self.position, (255, 50, 0))
        create_cloud(self.position, (255, 150, 0))

    def update(self, dt):
        self.shot_timer -= dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt)
        if keys[pygame.K_d]:
            self.rotate(-dt)

        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)

        if keys[pygame.K_SPACE]:
            if not (self.shot_timer > 0):
                self.shoot()

                self.shot_timer = SHOT_COOLDOWN