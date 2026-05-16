import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
import sys

def init():
    glClearColor(0.5, 0.8, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.33, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def draw_cube(color):
    """Cubo genérico para usar en varias partes"""
    glBegin(GL_QUADS)
    glColor3f(color[0], color[1], color[2])
    # Frente
    glVertex3f(-1, 0, 1); glVertex3f(1, 0, 1); glVertex3f(1, 1, 1); glVertex3f(-1, 1, 1)
    # Atrás
    glVertex3f(-1, 0, -1); glVertex3f(1, 0, -1); glVertex3f(1, 1, -1); glVertex3f(-1, 1, -1)
    # Arriba, Abajo, Izquierda, Derecha...
    glVertex3f(-1, 1, -1); glVertex3f(1, 1, -1); glVertex3f(1, 1, 1); glVertex3f(-1, 1, 1)
    glVertex3f(-1, 0, -1); glVertex3f(1, 0, -1); glVertex3f(1, 0, 1); glVertex3f(-1, 0, 1)
    glVertex3f(-1, 0, -1); glVertex3f(-1, 0, 1); glVertex3f(-1, 1, 1); glVertex3f(-1, 1, -1)
    glVertex3f(1, 0, -1); glVertex3f(1, 0, 1); glVertex3f(1, 1, 1); glVertex3f(1, 1, -1)
    glEnd()

def draw_details():
    """Puerta y Ventanas pegadas a la casa"""
    # Puerta (Negra/Marrón oscuro)
    glColor3f(0.2, 0.1, 0.0)
    glBegin(GL_QUADS)
    glVertex3f(-0.3, 0.01, 1.01) # Un pelín hacia adelante para que no parpadee
    glVertex3f(0.3, 0.01, 1.01)
    glVertex3f(0.3, 0.7, 1.01)
    glVertex3f(-0.3, 0.7, 1.01)
    glEnd()

    # Ventana (Azul claro)
    glColor3f(0.5, 0.9, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(0.5, 0.4, 1.01)
    glVertex3f(0.8, 0.4, 1.01)
    glVertex3f(0.8, 0.7, 1.01)
    glVertex3f(0.5, 0.7, 1.01)
    glEnd()

def draw_tree(x, z):
    """Dibuja un árbol en la posición x, z"""
    glPushMatrix()
    glTranslatef(x, 0, z)
    # Tronco
    glColor3f(0.4, 0.2, 0.0)
    glBegin(GL_QUADS)
    glVertex3f(-0.1, 0, 0.1); glVertex3f(0.1, 0, 0.1); glVertex3f(0.1, 0.8, 0.1); glVertex3f(-0.1, 0.8, 0.1)
    glEnd()
    # Hojas (Pirámide verde)
    glColor3f(0.0, 0.5, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex3f(-0.5, 0.8, 0.5); glVertex3f(0.5, 0.8, 0.5); glVertex3f(0, 1.8, 0)
    glVertex3f(-0.5, 0.8, -0.5); glVertex3f(0.5, 0.8, -0.5); glVertex3f(0, 1.8, 0)
    glVertex3f(-0.5, 0.8, -0.5); glVertex3f(-0.5, 0.8, 0.5); glVertex3f(0, 1.8, 0)
    glVertex3f(0.5, 0.8, -0.5); glVertex3f(0.5, 0.8, 0.5); glVertex3f(0, 1.8, 0)
    glEnd()
    glPopMatrix()

def draw_car():
    """Dibuja un carro amarillo simple"""
    glPushMatrix()
    glTranslatef(3, 0, 4) # Posición en el suelo
    glScalef(0.5, 0.5, 0.5)
    
    # Chasis (Caja de abajo)
    glPushMatrix()
    glScalef(2, 0.6, 1)
    draw_cube((1.0, 1.0, 0.0)) # Amarillo
    glPopMatrix()
    
    # Cabina (Caja de arriba)
    glPushMatrix()
    glTranslatef(0, 0.6, 0)
    glScalef(1, 0.6, 0.8)
    draw_cube((1.0, 1.0, 0.0))
    glPopMatrix()

    # Ruedas (Mini cubos negros)
    glColor3f(0, 0, 0)
    for rx, rz in [(-1.2, 0.8), (1.2, 0.8), (-1.2, -0.8), (1.2, -0.8)]:
        glPushMatrix()
        glTranslatef(rx, 0, rz)
        glScalef(0.3, 0.3, 0.3)
        draw_cube((0,0,0))
        glPopMatrix()
        
    glPopMatrix()

def draw_roof():
    glBegin(GL_TRIANGLES)
    glColor3f(0.9, 0.1, 0.1)
    glVertex3f(-1, 1, 1); glVertex3f(1, 1, 1); glVertex3f(0, 2, 0)
    glVertex3f(-1, 1, -1); glVertex3f(1, 1, -1); glVertex3f(0, 2, 0)
    glVertex3f(-1, 1, -1); glVertex3f(-1, 1, 1); glVertex3f(0, 2, 0)
    glVertex3f(1, 1, -1); glVertex3f(1, 1, 1); glVertex3f(0, 2, 0)
    glEnd()

def draw_ground():
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.6, 0.2) # Verde pasto
    glVertex3f(-10, 0, 10); glVertex3f(10, 0, 10); glVertex3f(10, 0, -10); glVertex3f(-10, 0, -10)
    # Calle (Gris)
    glColor3f(0.3, 0.3, 0.3)
    glVertex3f(2, 0.01, 10); glVertex3f(5, 0.01, 10); glVertex3f(5, 0.01, -10); glVertex3f(2, 0.01, -10)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(8, 6, 12, 0, 0, 0, 0, 1, 0)

    draw_ground()
    draw_cube((0.8, 0.5, 0.2)) # Casa
    draw_roof()
    draw_details() # Puerta y ventana
    
    # Dibujar varios árboles
    draw_tree(-4, -3)
    draw_tree(-5, 2)
    draw_tree(4, -5)
    
    draw_car() # Carro amarillo

    glfw.swap_buffers(window)

def main():
    global window
    if not glfw.init(): return
    window = glfw.create_window(800, 600, "Escena 3D Completa", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    init()
    while not glfw.window_should_close(window):
        display()
        glfw.poll_events()
    glfw.terminate()

if __name__ == "__main__":
    main()