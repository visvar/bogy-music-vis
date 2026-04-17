# Example file showing a circle moving on screen
import pygame
from pygame.locals import *
import pandas as pd
import sys, os
import cv2
import numpy as np
import subprocess
import math

window_size = (1280, 720)

# pygame setup
pygame.init()
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()
running = True
dt = 0

circle_position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

FALLBACK_WAV_FILE = os.path.join("audio", "HER.mp3")

if len(sys.argv) > 1:
    music_file = os.path.join("audio", sys.argv[1])  # Ensure file is in "audio" folder
else:
    music_file = FALLBACK_WAV_FILE  # Use fallback if no argument is given
pygame.mixer.music.load(music_file)
# load prepared data with audio features
if music_file.endswith('.wav'):
    data_file = music_file.replace('.wav', '.csv')
elif music_file.endswith('.mp3'):
    data_file = music_file.replace('.mp3', '.csv')
data = pd.read_csv(data_file)

print(f"loading finished for {music_file}")

# play and loop forever
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.7)


# Record video as output
output_file = data_file.replace('.csv', '_temp.mp4').replace('audio\\', '') 
video_file = data_file.replace('.csv', '.mp4').replace('audio\\', '') 

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
video = cv2.VideoWriter(output_file, fourcc, 60, window_size)

cmd = [
    "ffmpeg",
    "-y",
    "-i", output_file,
    "-i", music_file,
    "-c:v", "copy",
    "-c:a", "aac",
    "-shortest",
    video_file
]





# fade color
fade_color = (0, 0, 0, 80)
overlay = pygame.Surface(window_size, pygame.SRCALPHA)
overlay.fill(fade_color)

WIDTH, HEIGHT = 1280, 720
CENTER = (WIDTH // 2, HEIGHT // 2)

ball_x = WIDTH // 4

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    # fill the screen with a color to wipe away anything from last frame
    # screen.fill("black")
    screen.blit(overlay, (0, 0))


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

    if frame >= len(data)-1:
        running = False
        break

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

    chroma_labels = ["chroma_C", "chroma_C#", "chroma_D", "chroma_D#", "chroma_E",
                 "chroma_F", "chroma_F#", "chroma_G", "chroma_G#", "chroma_A",
                 "chroma_A#", "chroma_B"]
    # Bar Chart Settings
    BAR_WIDTH = WIDTH // len(chroma_labels)
    MAX_BAR_HEIGHT = HEIGHT // 3



    # =========================================================
    # 📊 VERTICAL BEAT BOUNCE METER (BOTTOM ↔ TOP)
    # =========================================================

    since = frames_since_last_beat
    until = max(frames_until_next_beat, 1)

    total = since + until

    # normalized beat cycle (0 → 1 → 0)
    t = since / total

    # bounce curve: bottom → top → bottom
    bounce = math.sin(t * math.pi)

    bar_height = HEIGHT
    bar_width = 12

    x_pos = WIDTH - 40

    # fill height based on bounce (true up/down motion)
    fill_height = int(bar_height * bounce)

    # background
    pygame.draw.rect(
        screen,
        (30, 30, 30),
        (x_pos, 0, bar_width, bar_height)
    )

    # fill (moves bottom ↔ top)
    pygame.draw.rect(
        screen,
        (230, 230, 230),
        (x_pos, HEIGHT - fill_height, bar_width, fill_height)
    )

    # =========================================================
    # 📊 CHROMA BAR CHART
    # =========================================================

    for i, label in enumerate(chroma_labels):
        value = features[label]
        bar_height = int((value / 10) * MAX_BAR_HEIGHT)

        color = (
            int(128 + 127 * math.sin(i)),
            int(128 + 127 * math.sin(i + 2)),
            int(128 + 127 * math.sin(i + 4)),
        )

        x = i * BAR_WIDTH

        # TOP bars
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect((x, 0), (BAR_WIDTH - 4, bar_height))
        )

        # BOTTOM bars
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect((x, HEIGHT - bar_height), (BAR_WIDTH - 4, bar_height))
        )


    # =========================================================
    # ⚡ ENERGY CORE (SHIFTED TO 2/3 WIDTH CENTER)
    # =========================================================
    core_x = int((WIDTH * 2) / 3)
    core_y = HEIGHT // 2

    pulse_radius = int(50 + energy * 300)

    pygame.draw.circle(
        screen,
        (
            min(255, int(brightness / 20)),
            min(255, int(100 + energy * 100)),
            255
        ),
        (core_x, core_y),
        pulse_radius,
        3
    )


    # =========================================================
    # 🌊 FREQUENCY-DRIVEN WAVE (SINGLE FUNDAMENTAL)
    # =========================================================

    mid_y = HEIGHT // 2
    start_x = 0
    end_x = int(WIDTH * 2 / 3)

    time_factor = pygame.time.get_ticks() * 0.01  # speed

    # --- get frequency ---
    freq = fundamental_frequencies

    # clamp to avoid extreme visuals
    freq = max(50, min(freq, 2000))

    # convert Hz → visual scale (VERY important tuning)
    scale = freq / 300   # <-- tweak this (200–500 range works well)

    # amplitude from energy (keeps it dynamic)
    amplitude = 20 + energy * 200

    for i in range(start_x, end_x, 4):

        y = int(
            mid_y +
            math.sin(i * 0.02 * scale - time_factor) * amplitude
        )

        pygame.draw.circle(
            screen,
            (
                180,
                min(255, 100 + int(energy * 155)),
                255
            ),
            (i, y),
            2
        )


    # =========================================================
    # MFCC ORBIT FIELD (CENTERED AROUND CORE)
    # =========================================================
    for i in range(13):
        mfcc = features[f"mfcc_{i}"]

        angle = pygame.time.get_ticks() * 0.001 + i
        radius = 130 + mfcc

        x = int(core_x + math.cos(angle) * radius)
        y = int(core_y + math.sin(angle) * radius)

        size = int(abs(mfcc))/5

        pygame.draw.circle(
            screen,
            (
                min(255, 120 + i * 10),
                min(255, 50 + abs(mfcc) * 20),
                200
            ),
            (x, y),
            max(4, size)
        )


    # =========================================================
    # 💥 BEAT IMPACT (CORE-BASED SHOCK)
    # =========================================================
    high_energy = energy > 0.8

    if frames_until_next_beat == 1 and high_energy:

        # shock rings
        for r in range(0, 300, 12):
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (core_x, core_y),
                r,
                2
            )

        # burst
        for i in range(13):
            angle = i * (2 * math.pi / 13)
            speed = 6 + abs(features[f"mfcc_{i}"]) * 2

            dx = math.cos(angle) * speed * 12
            dy = math.sin(angle) * speed * 12

            px = core_x + dx
            py = core_y + dy

            pygame.draw.circle(
                screen,
                (255, 200, 255),
                (int(px), int(py)),
                4
            )

    
    
    # =========================================================
    # 🟡 BALL ON YOUR EXACT WAVE
    # =========================================================

    # --- movement (A/D only) ---
    move_speed = 500 * dt

    if keys[pygame.K_a]:
        ball_x -= move_speed
    if keys[pygame.K_d]:
        ball_x += move_speed

    # clamp inside wave region
    wave_end = int(WIDTH * 2 / 3)
    ball_x = max(0, min(wave_end, ball_x))

    # ---------- SAME WAVE MATH ----------
    mid_y = HEIGHT // 2
    time_factor = pygame.time.get_ticks() * 0.01

    freq = fundamental_frequencies
    freq = max(50, min(freq, 2000))

    scale = freq / 300
    amplitude = 20 + energy * 200

    # EXACT SAME FORMULA (i → ball_x)
    ball_y = mid_y + math.sin(ball_x * 0.02 * scale - time_factor) * amplitude


    # --- draw ball ---
    pygame.draw.circle(
        screen,
        (255, 255, 100),
        (int(ball_x), int(ball_y)),
        10
    )


    # ---------- DISPLAY ----------
    pygame.display.flip()
    dt = clock.tick(60) / 1000

    # inside game loop
    frame = pygame.surfarray.array3d(screen)
    frame = np.transpose(frame, (1, 0, 2))  # Pygame -> OpenCV format
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    video.write(frame)

print('video saved as output.mp4')
video.release()
subprocess.run(cmd)
if os.path.exists(output_file):
    os.remove(output_file)
pygame.quit()
