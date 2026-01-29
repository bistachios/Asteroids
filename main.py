import pygame
from player import Player
from asteroid import Asteroid
from shot import Shot
from asteroidfield import AsteroidField
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_RADIUS, LINE_WIDTH, PLAYER_IFRAME_DURATION
from logger import log_state, log_event
import sys

def main():

	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	background = pygame.image.load("assets/images/spaceBG1.jpg")
	background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
	clock = pygame.time.Clock()
	dt = 0

	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()
	asteroids = pygame.sprite.Group()
	shots = pygame.sprite.Group()

	score = 0
	shield = 100
	player_invincible_timer = 0
	font = pygame.font.Font("assets/fonts/Orbitron.ttf", 36)

	game_state = "MENU"

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

			if game_state == "MENU":
				if event.type == pygame.KEYDOWN:
					if event.key in (pygame.K_RETURN, pygame.K_SPACE):
						game_state = "GAME"

		if game_state == "GAME":
			updatable.update(dt)
		
			if player_invincible_timer > 0:
				player_invincible_timer -=1

			for obj in asteroids:
				if obj.collides_with(player) and player_invincible_timer <= 0:
					log_event("player_hit")
					obj.kill()
					shield -= 25
					player_invincible_timer = PLAYER_IFRAME_DURATION
					if shield == 0:
						print("Game over!")
						sys.exit()

			for asteroid in asteroids:
				for shot in shots:
					if shot.collides_with(asteroid):
						log_event("asteroid_shot")
						score += 100
						asteroid.split()
						shot.kill()

		screen.blit(background, (0, 0))

		if game_state == "MENU":
				title_font = pygame.font.Font("assets/fonts/Orbitron.ttf", 72)
				small_font = pygame.font.Font("assets/fonts/Orbitron.ttf", 32)

				title_surf = title_font.render("ASTEROIDS", True, "white")
				prompt_surf = small_font.render("Press ENTER or SPACE to start", True, "white")

				title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
				prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))

				screen.blit(title_surf, title_rect)
				screen.blit(prompt_surf, prompt_rect)

		elif game_state == "GAME":

				for obj in drawable:
					obj.draw(screen)

				score_surf = font.render(f"Score: {score}", True, "white")
				screen.blit(score_surf, (10, 10))


				if shield > 25:
					shield_surf = font.render(f"Shield: {shield}%", True, "white")
				else:
					shield_surf = font.render(f"Shield: {shield}%", True, "red")
				x_pos = SCREEN_WIDTH - shield_surf.get_width() - 10
				y_pos = 10
				screen.blit(shield_surf, (x_pos, y_pos))

		pygame.display.flip()
		dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
