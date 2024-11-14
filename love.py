import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load heartbeat sound
heartbeat_sound = pygame.mixer.Sound('heartbeat-loop.mp3')

# Set up display
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Set up OpenGL
glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
glTranslatef(0.0, 0.0, -10)  # Move the camera back a bit

# Function to draw 3D heart shape
def draw_heart(scale, thickness):
    glBegin(GL_TRIANGLES)
    for s in np.linspace(0, np.pi, 100):
        for t in np.linspace(0, 2 * np.pi, 100):
            # Parametric equation of heart shape
            x1 = scale * 16 * np.sin(s) ** 3
            y1 = scale * (13 * np.cos(s) - 5 * np.cos(2 * s) - 2 * np.cos(3 * s) - np.cos(4 * s))
            z1 = scale * 16 * np.sin(s) * np.cos(t)
            
            # Pulsing effect based on sine wave
            y1 += 0.2 * np.sin(5 * s) * scale  # Adding more pulsation for smoothness

            glColor3f(1, 0, 0)  # Set color to red (heart color)
            glVertex3f(x1, y1, z1)

            # Simulating thickness of the heart by adding another triangle
            x2 = x1
            y2 = y1 + thickness  # Increase y for the thickness effect
            z2 = z1

            glColor3f(1, 0.5, 0.5)  # Lighter color for thickness
            glVertex3f(x2, y2, z2)

    glEnd()

# Animation loop
scale = 0.4
scale_direction = 0.02
thickness = 0.1  # Change thickness for a better 3D effect
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Animate the heart (change the scale for pulsing effect)
    scale += scale_direction
    if scale >= 1.1 or scale <= 0.7:
        scale_direction = -scale_direction
        if not pygame.mixer.get_busy():  # Check if the sound is not already playing
            heartbeat_sound.play()

    # Draw the first heart (center)
    glPushMatrix()
    glScalef(scale, scale, scale)
    draw_heart(scale, thickness)
    glPopMatrix()

    # Draw the second heart (right side, rotated to face left)
    glPushMatrix()
    glRotatef(180, 0, 1, 0)  # Rotate the second heart by 180 degrees around the Y-axis to face the left
    glScalef(scale, scale, scale)
    draw_heart(scale, thickness)
    glPopMatrix()

    # Update the display
    pygame.display.flip()
    pygame.time.wait(20)  # Longer wait for smoother animation

# Quit Pygame
pygame.quit()
