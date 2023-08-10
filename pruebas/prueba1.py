import pygame
import sys
import numpy as np
from moviepy.editor import ImageSequenceClip

pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Animation")

# Colors
WHITE = (255, 255, 255)

clock = pygame.time.Clock()

running = True

x, y = 100, 100
velocity = 5

# Create a list to store frames
frames = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= velocity
    if keys[pygame.K_RIGHT]:
        x += velocity
    if keys[pygame.K_UP]:
        y -= velocity
    if keys[pygame.K_DOWN]:
        y += velocity

    screen.fill(WHITE)
    pygame.draw.circle(screen, (0, 0, 255), (x, y), 30)
    pygame.display.flip()

    # Capture the frame and add it to the frames list
    frame = pygame.surfarray.array3d(screen)

    rotated_frame = np.rot90(frame, k=-1)
    flipped_frame = np.fliplr(rotated_frame)

    frames.append(flipped_frame)

    clock.tick(30)

pygame.quit()

# Create the video using moviepy
fps = 30
video_clip = ImageSequenceClip(frames, fps=fps)
video_clip.write_videofile("animation_output.mp4", fps=fps)

sys.exit()
