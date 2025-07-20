from circleshape import CircleShape
from shot import Shot
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_MOVE_SPEED, PLAYER_SHOOT_SPEED, SHOT_COOLDOWN, \
    FIRE_RATE_DURATION, SPEED_DURATION
import pygame
from particle import create_cloud


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0

        self.shot_timer = 0
        self.immune_timer = 0
        self.fire_rate_timer = 0
        self.speed_timer = 0

        self.dying = False
        self.shielded = False

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
            if self.shielded:
                color = (0, 0, 255)
            elif self.immune_timer > 0:
                color = (102, 102, 102)
            elif self.fire_rate_timer > 0:
                blue = 255 - (255 * (self.fire_rate_timer / FIRE_RATE_DURATION))

                color = (255, 255, int(blue))
            elif self.speed_timer > 0:
                red = 255 - (255 * (self.speed_timer / SPEED_DURATION))
                blue = 255 - (255 * (self.speed_timer / SPEED_DURATION))

                color = (int(red), 255, int(blue))
            else:
                color = "white"

            pygame.draw.polygon(screen, color, self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        start = pygame.Vector2(0, 1)
        start = start.rotate(self.rotation)

        start *= PLAYER_MOVE_SPEED * dt

        if self.speed_timer > 0:
            start *= 3

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
        self.fire_rate_timer -= dt
        self.speed_timer -= dt

        if not self.shielded:
            self.immune_timer -= dt

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

                if self.fire_rate_timer <= 0:
                    self.shot_timer = SHOT_COOLDOWN
                else:
                    self.shot_timer = SHOT_COOLDOWN / 2