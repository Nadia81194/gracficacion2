import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

rotation = 0.0

def draw_sphere(radius, slices=30, stacks=30):
    """Misión 2: Función con normales para que la luz rebote bien"""
    quad = gluNewQuadric()
    # Misión 2: Generar normales suaves para que se vea redondito
    gluQuadricNormals(quad, GLU_SMOOTH) 
    gluSphere(quad, radius, slices, stacks)
    gluDeleteQuadric(quad)

def set_material(amb, diff, spec, shine):
    """Misión 3: Función para cambiar las propiedades del material"""
    glMaterialfv(GL_FRONT, GL_AMBIENT, amb)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diff)
    glMaterialfv(GL_FRONT, GL_SPECULAR, spec)
    glMaterialf(GL_FRONT, GL_SHININESS, shine)

def draw_eye():
    glPushMatrix()
    
    # Misión 4: Usamos glColor para el color base (Ambient y Diffuse)
    # pero el brillo (Specular) lo define el material.

    # 1. PIEL 
    glColor3f(0.85, 0.67, 0.65)
    set_material([0.2, 0.2, 0.2, 1.0], [0.8, 0.8, 0.8, 1.0], [0.1, 0.1, 0.1, 1.0], 5)
    glPushMatrix()
    glTranslatef(0.7, 0, 0)
    draw_sphere(0.54)
    glPopMatrix()

    # 2. BLANCO 
    glColor3f(1.0, 1.0, 1.0)
    set_material([0.2, 0.2, 0.2, 1.0], [1.0, 1.0, 1.0, 1.0], [0.9, 0.9, 0.9, 1.0], 100)
    glPushMatrix()
    glTranslatef(0.56, 0, 0)
    draw_sphere(0.6)
    glPopMatrix()

    # 3. IRIS 
    glColor3f(0.2, 0.4, 0.8) # Azulito
    set_material([0.1, 0.1, 0.1, 1.0], [0.8, 0.8, 0.8, 1.0], [0.4, 0.4, 0.4, 1.0], 30)
    glPushMatrix()
    glTranslatef(0.49, 0, 0)
    draw_sphere(0.55)
    glPopMatrix()

    # 4. PUPILA 
    glColor3f(0.0, 0.0, 0.0)
    set_material([0.0, 0.0, 0.0, 1.0], [0.1, 0.1, 0.1, 1.0], [0.0, 0.0, 0.0, 1.0], 1)
    glPushMatrix()
    glTranslatef(0.3, 0, 0)
    draw_sphere(0.4)
    glPopMatrix()

    glPopMatrix()

def setup_lighting():
    """Misión 1: Configuración de luces"""
    # Activamos la iluminación general
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST) # Para que las cosas de atrás no se vean adelante

    # Colores de la luz (Blanca)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    # Misión 4: Permitir que glColor3f controle el material automáticamente
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

def main():
    global rotation
    if not glfw.init():
        return
    window = glfw.create_window(800, 600, "Misión: Ojo 3D Iluminado", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    
    glClearColor(0.1, 0.1, 0.1, 1.0) # Fondo oscuro para que resalte la luz
    setup_lighting()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800/600, 0.1, 100.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Misión 5 (Opción A): Luz fija en el mundo
        # Si ponemos la posición aquí, la luz no gira con el ojo
        light_pos = [2.0, 2.0, 2.0, 1.0] # 1.0 = Luz posicional (como una lámpara)
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
        
        glTranslatef(0, 0, -5)
        rotation += 0.5
        glRotatef(rotation, 0, 1, 0)
        
        draw_eye()
        
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()