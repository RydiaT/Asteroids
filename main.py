import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from sys import exit
from colorama import init
from helpers import cprint, get_highscore, set_highscore, on_exit
from particle import Particle

init()

def main():
	cprint("\nStarting Asteroids!", "info")

	print("\n=====================================\n")

	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

	score_font = pygame.font.SysFont('Arial', 36)  # Using a system font, size 36
	highscore_font = pygame.font.SysFont('Arial', 20)  # Using a system font, size 36


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
	Particle.containers = (updatable, drawable)

	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
	field = AsteroidField()

	score = 0
	highscore = get_highscore()

	death_timer = 0

	while True:
		# Lets us actually use the [X] button
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				on_exit(score, highscore)
				return
		# Update
		updatable.update(dt)

		if not player.dying:
			for thing in asteroids:
				if thing.is_colliding(player):
					on_exit(score, highscore)
					player.game_over()

					death_timer = PLAYER_DEATH_TIMER
					player.dying = True

			for thing in asteroids:
				for bullet in shots:
					if thing.is_colliding(bullet):
						thing.split()
						bullet.kill()

						score += 1
		else:
			death_timer -= dt

		if death_timer <= 0 and player.dying:
			cprint("Game over!", "error")

			exit()

		# Render
		screen.fill("black")

		if score > highscore:
			text_color = "yellow"
		else:
			text_color = "white"

		score_surface = score_font.render(f"{score}", True, text_color)
		score_rext = score_surface.get_rect()
		score_rext.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Center it on the screen

		highscore_surface = highscore_font.render(f"{highscore}", True, "grey")
		highscore_rext = highscore_surface.get_rect()
		highscore_rext.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 25)  # Center it on the screen

		screen.blit(score_surface, score_rext)
		screen.blit(highscore_surface, highscore_rext)

		for thing in drawable:
			thing.draw(screen)

		# ALWAYS GOES LAST
		pygame.display.flip()
		dt = clock.tick(60) / 1000

if __name__ == "__main__":
	main()