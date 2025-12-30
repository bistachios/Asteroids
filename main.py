import pygame
from player import Player
from asteroid import Asteroid
from shot import Shot
from asteroidfield import AsteroidField
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_RADIUS, LINE_WIDTH
from logger import log_state, log_event
import sys

def main():
	print("Starting Asteroids with pygame version: 2.6.1")
	print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")

	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	clock = pygame.time.Clock()
	dt = 0

	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()
	asteroids = pygame.sprite.Group()
	shots = pygame.sprite.Group()

	score = 0
	font = 

	Player.containers = (updatable, drawable)
	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

	Asteroid.containers = (asteroids, updatable, drawable)

	Shot.containers = (shots, updatable, drawable)

	AsteroidField.containers = (updatable)

	asteroid_field = AsteroidField()

	while True:
		log_state()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
        			return

		updatable.update(dt)

		for obj in asteroids:
			if obj.collides_with(player):
				log_event("player_hit")
				print("Game over!")
				sys.exit()

		for asteroid in asteroids:
			for shot in shots:
				if shot.collides_with(asteroid):
					log_event("asteroid_shot")
					score += 100
					asteroid.split()
					shot.kill()

		screen.fill("black")

		for obj in drawable:
			obj.draw(screen)

		pygame.display.flip()
		dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
