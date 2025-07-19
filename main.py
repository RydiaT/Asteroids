import os.path

import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from sys import exit

def get_highscore():
	if not os.path.exists("highscore.txt"):
		print("No highscore file found.")
		f = open("highscore.txt", "x")
		f = open("highscore.txt", "w")
		f.write("0")
		f.close()
		print("Highscore save created.")
		print("\n=====================================\n")

	with open("highscore.txt", "r") as score_raw:
		score = score_raw.read().strip()

		try:
			return int(score)
		except ValueError:
			print("Highscore unable to be read.")
			print(score)
			print(type(score))
			return -1

def set_highscore(score):
	with open("highscore.txt", "w") as score_raw:
		score_raw.write(f"{score}")



def main():
	print("\nStarting Asteroids!")

	print("\n=====================================\n")

	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

	font = pygame.font.SysFont('Arial', 36)  # Using a system font, size 36

	clock = pygame.time.Clock()
	dt = 0

	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()
	asteroids = pygame.sprite.Group()
	shots = pygame.sprite.Group()

	Player.containers = (updatable, drawable)
	Asteroid.containers = (asteroids, updatable, drawable)
	AsteroidField.containers = (updatable,)
	Shot.containers = (shots, updatable, drawable)

	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
	field = AsteroidField()

	score = 0
	highscore = get_highscore()

	while True:
		# Lets us actually use the [X] button
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
		# Update
		updatable.update(dt)

		for thing in asteroids:
			if thing.is_colliding(player):
				if score > highscore:
					print("NEW HIGHSCORE!!!!")
					print(f"{highscore} ---> {score}")

					set_highscore(score)

				exit("Game over!")

		for thing in asteroids:
			for bullet in shots:
				if thing.is_colliding(bullet):
					thing.split()
					bullet.kill()

					score += 1

		# Render
		screen.fill("black")

		if score > highscore:
			text_color = "yellow"
		else:
			text_color = "white"

		text_surface = font.render(f"{score}", True, text_color)
		text_rect = text_surface.get_rect()
		text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Center it on the screen

		screen.blit(text_surface, text_rect)

		for thing in drawable:
			thing.draw(screen)

		# ALWAYS GOES LAST
		pygame.display.flip()
		dt = clock.tick(60) / 1000

if __name__ == "__main__":
	main()