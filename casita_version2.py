import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
import sys
import random

window = None

def init():
    glClearColor(0.4, 0.7, 1.0, 1.0) 
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.33, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def draw_textured_cube(color, scale=(1,1,1)):
    glPushMatrix()
    glScalef(scale[0], scale[1], scale[2])
    glBegin(GL_QUADS)
    for i in range(6):
        tonalidad = 0.8 + (i * 0.04) 
        glColor3f(color[0]*tonalidad, color[1]*tonalidad, color[2]*tonalidad)
        if i == 0: # Frente
            glVertex3f(-1, 0, 1); glVertex3f(1, 0, 1); glVertex3f(1, 1, 1); glVertex3f(-1, 1, 1)
        elif i == 1: # Atras
            glVertex3f(-1, 0, -1); glVertex3f(1, 0, -1); glVertex3f(1, 1, -1); glVertex3f(-1, 1, -1)
        elif i == 2: # Arriba
            glVertex3f(-1, 1, -1); glVertex3f(1, 1, -1); glVertex3f(1, 1, 1); glVertex3f(-1, 1, 1)
        elif i == 3: # Abajo
            glVertex3f(-1, 0, -1); glVertex3f(1, 0, -1); glVertex3f(1, 0, 1); glVertex3f(-1, 0, 1)
        elif i == 4: # Izquierda
            glVertex3f(-1, 0, -1); glVertex3f(-1, 0, 1); glVertex3f(-1, 1, 1); glVertex3f(-1, 1, -1)
        elif i == 5: # Derecha
            glVertex3f(1, 0, -1); glVertex3f(1, 0, 1); glVertex3f(1, 1, 1); glVertex3f(1, 1, -1)
    glEnd()
    glPopMatrix()

def draw_house(x, z, color):
    glPushMatrix()
    glTranslatef(x, 0, z)
    
    # 1. Cuerpo de la casa
    draw_textured_cube(color)
    
    # 2. Puerta (Frente)
    glColor3f(0.2, 0.1, 0.0)
    glBegin(GL_QUADS)
    glVertex3f(-0.25, 0, 1.01); glVertex3f(0.25, 0, 1.01); glVertex3f(0.25, 0.7, 1.01); glVertex3f(-0.25, 0.7, 1.01)
    glEnd()

    # 3. Ventanas (Frente)
    glColor3f(0.6, 0.9, 1.0)
    glBegin(GL_QUADS)
    # Ventana Izquierda
    glVertex3f(-0.8, 0.4, 1.01); glVertex3f(-0.4, 0.4, 1.01); glVertex3f(-0.4, 0.8, 1.01); glVertex3f(-0.8, 0.8, 1.01)
    # Ventana Derecha
    glVertex3f(0.4, 0.4, 1.01); glVertex3f(0.8, 0.4, 1.01); glVertex3f(0.8, 0.8, 1.01); glVertex3f(0.4, 0.8, 1.01)
    glEnd()

    # 4. Techo
    glBegin(GL_TRIANGLES)
    glColor3f(0.6, 0.1, 0.1)
    glVertex3f(-1.1, 1, 1.1); glVertex3f(1.1, 1, 1.1); glVertex3f(0, 2, 0)
    glVertex3f(-1.1, 1, -1.1); glVertex3f(1.1, 1, -1.1); glVertex3f(0, 2, 0)
    glVertex3f(-1.1, 1, -1.1); glVertex3f(-1.1, 1, 1.1); glVertex3f(0, 2, 0)
    glVertex3f(1.1, 1, -1.1); glVertex3f(1.1, 1, 1.1); glVertex3f(0, 2, 0)
    glEnd()
    glPopMatrix()

def draw_tree(x, z):
    glPushMatrix()
    glTranslatef(x, 0, z)
    draw_textured_cube((0.3, 0.15, 0.05), scale=(0.1, 0.8, 0.1))
    glTranslatef(0, 0.8, 0)
    glColor3f(0.1, 0.4, 0.1)
    for i in range(3):
        glPushMatrix()
        glTranslatef(0, i * 0.3, 0)
        glBegin(GL_TRIANGLES)
        glVertex3f(-0.6, 0, 0.6); glVertex3f(0.6, 0, 0.6); glVertex3f(0, 0.8, 0)
        glVertex3f(-0.6, 0, -0.6); glVertex3f(0.6, 0, -0.6); glVertex3f(0, 0.8, 0)
        glVertex3f(-0.6, 0, -0.6); glVertex3f(-0.6, 0, 0.6); glVertex3f(0, 0.8, 0)
        glVertex3f(0.6, 0, -0.6); glVertex3f(0.6, 0, 0.6); glVertex3f(0, 0.8, 0)
        glEnd()
        glPopMatrix()
    glPopMatrix()

def draw_car(x, z, color):
    glPushMatrix()
    glTranslatef(x, 0.1, z)
    glScalef(0.4, 0.4, 0.4)
    draw_textured_cube(color, scale=(1.8, 0.5, 0.8)) 
    glTranslatef(0, 0.5, 0)
    draw_textured_cube((0.7, 0.9, 1.0), scale=(0.9, 0.5, 0.7))
    glPopMatrix()

def draw_city():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
 
    gluLookAt(25, 20, 25, 0, 0, 0, 0, 1, 0)
    glColor3f(0.2, 0.5, 0.2)
    glBegin(GL_QUADS)
    glVertex3f(-30, 0, 30); glVertex3f(30, 0, 30); glVertex3f(30, 0, -30); glVertex3f(-30, 0, -30)
    glEnd()

    # Calle
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_QUADS)
    glVertex3f(-30, 0.01, 3); glVertex3f(30, 0.01, 3); glVertex3f(30, 0.01, -3); glVertex3f(-30, 0.01, -3)
    glEnd()

    #  Casas 
    colores_casa = [(0.8, 0.5, 0.2), (0.2, 0.5, 0.8), (0.7, 0.3, 0.7), (0.4, 0.7, 0.4), (0.9, 0.8, 0.6)]
    for i in range(5):
        draw_house(-15 + (i*7), 6, colores_casa[i % 5])
        glPushMatrix()
        glTranslatef(-15 + (i*7), 0, -6)
        glRotatef(180, 0, 1, 0)
        draw_house(0, 0, colores_casa[(i+2) % 5])
        glPopMatrix()

    # Árboles
    random.seed(42)
    for _ in range(30):
        tx = random.uniform(-25, 25)
        tz = random.choice([random.uniform(9, 20), random.uniform(-20, -9)])
        draw_tree(tx, tz)

    # Carros
    for i in range(6):
        draw_car(-20 + (i*8), 1.5, (1, 1, 0)) # Amarillos
        draw_car(-15 + (i*8), -1.5, (1, 0, 0)) # Rojos

    glfw.swap_buffers(window)

def main():
    global window
    if not glfw.init(): return
    window = glfw.create_window(1000, 700, "Ciudad Vista de Dron", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    init()
    while not glfw.window_should_close(window):
        draw_city()
        glfw.poll_events()
    glfw.terminate()

if __name__ == "__main__":
    main()