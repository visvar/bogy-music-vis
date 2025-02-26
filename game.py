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


music_file = "./audio/IRIS.wav"
pygame.mixer.music.load(music_file)
# load prepared data with audio features
data_file = music_file.replace(".wav", ".csv")
data = pd.read_csv(data_file)

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

    features = data.iloc[frame]

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
    mfcc_0= features["mfcc_0"]
    mfcc_1= features["mfcc_1"]
    mfcc_2= features["mfcc_2"]
    mfcc_3= features["mfcc_3"]
    mfcc_4= features["mfcc_4"]
    mfcc_5= features["mfcc_5"]
    mfcc_6= features["mfcc_6"]
    mfcc_7= features["mfcc_7"]
    mfcc_8= features["mfcc_8"]
    mfcc_9= features["mfcc_9"]
    mfcc_10= features["mfcc_10"]
    mfcc_11= features["mfcc_11"]
    mfcc_12= features["mfcc_12"]


    WIDTH, HEIGHT = 800, 600
    chroma_labels = ["chroma_C", "chroma_C#", "chroma_D", "chroma_D#", "chroma_E", 
                 "chroma_F", "chroma_F#", "chroma_G", "chroma_G#", "chroma_A", 
                 "chroma_A#", "chroma_B"]
    # Bar Chart Settings
    BAR_WIDTH = WIDTH // len(chroma_labels)
    MAX_BAR_HEIGHT = HEIGHT // 2
    # Draw bars
    for i, value in enumerate(chroma_labels):
        bar_height = int((features[value] / 10) * MAX_BAR_HEIGHT)
        pygame.draw.rect(screen, (0, 255, 0), 
                         (i * BAR_WIDTH, HEIGHT - bar_height, BAR_WIDTH - 5, bar_height))

    # Flash Effect
    flash_size = int(energy * 800)  # Larger flash with higher energy
    flash_brightness = min(255, int((brightness / 5000) * 255))


    flash_color = (flash_brightness, flash_brightness, flash_brightness)  # White flash

    
    pygame.draw.circle(screen, flash_color, circle_position, flash_size)


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()
