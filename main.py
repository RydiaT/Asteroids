import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField


def main():
	print("Starting Asteroids!")
	print(f"Screen width: {SCREEN_WIDTH}")
	print(f"Screen height: {SCREEN_HEIGHT}")

	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

	clock = pygame.time.Clock()
	dt = 0

	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()
	asteroids = pygame.sprite.Group()

	Player.containers = (updatable, drawable)
	Asteroid.containers = (asteroids, updatable, drawable)
	AsteroidField.containers = (updatable,)

	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
	field = AsteroidField()

	while True:
		# Lets us actually use the [X] button
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
		# Update
		updatable.update(dt)

		# Render
		screen.fill("black")

		for thing in drawable:
			thing.draw(screen)

		# ALWAYS GOES LAST
		pygame.display.flip()
		dt = clock.tick(60) / 1000

if __name__ == "__main__":
	main()