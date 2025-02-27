# Example file showing a circle moving on screen
import pygame
from pygame.locals import *
import pandas as pd
import math

window_size = (1280, 720)

# pygame setup
pygame.init()
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()
running = True
dt = 0

circle_position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


music_file = "./audio/pixlaxdax.wav"
pygame.mixer.music.load(music_file)
# load prepared data with audio features
data_file = music_file.replace(".wav", ".csv")
data = pd.read_csv(data_file)

print(f"loading finished for {music_file}")

# play and loop forever
pygame.mixer.music.play(-1)


overlay = pygame.Surface(window_size, pygame.SRCALPHA)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    # keyboard input
    #pygame.draw.circle(screen, "cyan", circle_position, 40)
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
    frame = int(seconds * 60)
    step = 1
    steps = 80
    for f in range(0, steps):

        if frame-f*step < 0:
            break
        features = data.iloc[frame-(steps-f)*step]

        energy = features["energy"]
        brightness = features["brightness"]
        fundamental_frequencies = features["fundamental_frequencies"]
        frames_since_last_beat= features["frames_since_last_beat"]
        frames_until_next_beat= features["frames_until_next_beat"]
        chroma_C= features["chroma_C"]
        chroma_Cs= features["chroma_C#"]
        chroma_D= features["chroma_D"]
        chroma_Ds= features["chroma_D#"]
        chroma_E= features["chroma_E"]
        chroma_F= features["chroma_F"]
        chroma_Fs= features["chroma_F#"]
        chroma_G= features["chroma_G"]
        chroma_Gs= features["chroma_G#"]
        chroma_A= features["chroma_A"]
        chroma_As= features["chroma_A#"]
        chroma_B= features["chroma_B"]

        chroma_labels = ["chroma_C", "chroma_C#", "chroma_D", "chroma_D#", "chroma_E",
                    "chroma_F", "chroma_F#", "chroma_G", "chroma_G#", "chroma_A",
                    "chroma_A#", "chroma_B"]
        # Bar Chart Settings
        x_step = 15
        max_radius = window_size[1] / 13
        # fade
        # fade color
        if energy < 10:
            fade_color = (8, 16, 0, 16)
        else:
            fade_color = (16, 8, 0, 16)

        overlay.fill(fade_color)
        screen.blit(overlay, (0, 0))
        # Draw bars
        for i, value in enumerate(chroma_labels):
            r = int((features[value] / 4) * max_radius)
            # curve up/down depending on time
            curve = math.sin(seconds*8*(60/132)) * (steps-f) * (6-i)/10
            x = window_size[0] -f * x_step + math.cos(i/6*math.pi)*30
            y = max_radius*(i+1)-r
            pygame.draw.ellipse(screen,
                            (255, 255, 0),
                            (x,
                             y+curve,
                             r,
                             r*2))


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()
