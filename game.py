# Example file showing a circle moving on screen
import pygame
from pygame.locals import *
import pandas as pd


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

circle_position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


music_file = "../audio/happinezz.mp3"
pygame.mixer.music.load(music_file)
# load prepared data with audio features
# data = pd.read_csv(music_file + "_data.csv").values

print(f"loading finished for {music_file}")

# play and loop forever
pygame.mixer.music.play(-1)




while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")


    # keyboard input
    pygame.draw.circle(screen, "cyan", circle_position, 40)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        circle_position.y -= 300 * dt
    if keys[pygame.K_s]:
        circle_position.y += 300 * dt
    if keys[pygame.K_a]:
        circle_position.x -= 300 * dt
    if keys[pygame.K_d]:
        circle_position.x += 300 * dt

    # mouse input
    mouse_x, mouse_y = pygame.mouse.get_pos()
    print(mouse_x, mouse_y)
    is_pressed = pygame.mouse.get_pressed()[0]
    if is_pressed:
        radius = 20
    else:
        radius = 10
    pygame.draw.circle(screen, "lime", pygame.mouse.get_pos(), radius)

    # music time
    time = pygame.mixer.music.get_pos()
    seconds = time/1000

    # get current music features
    frame = time * 60
    # features = data[frame]


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()
