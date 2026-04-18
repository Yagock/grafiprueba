import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

# Variables globales
window = None
angle = 0

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)

def cube():
    glBegin(GL_QUADS)

    # Cara superior
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f( 1, 1,-1)
    glVertex3f(-1, 1,-1)
    glVertex3f(-1, 1, 1)
    glVertex3f( 1, 1, 1)

    # Cara inferior
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f( 1,-1, 1)
    glVertex3f(-1,-1, 1)
    glVertex3f(-1,-1,-1)
    glVertex3f( 1,-1,-1)

    # Cara frontal
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f( 1, 1, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1,-1, 1)
    glVertex3f( 1,-1, 1)

    # Cara trasera
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f( 1,-1,-1)
    glVertex3f(-1,-1,-1)
    glVertex3f(-1, 1,-1)
    glVertex3f( 1, 1,-1)

    # Cara izquierda
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, 1,-1)
    glVertex3f(-1,-1,-1)
    glVertex3f(-1,-1, 1)

    # Cara derecha
    glColor3f(0.0, 1.0, 1.0)
    glVertex3f( 1, 1,-1)
    glVertex3f( 1, 1, 1)
    glVertex3f( 1,-1, 1)
    glVertex3f( 1,-1,-1)

    glEnd()

def draw_scene():
    global angle

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Cubo 1 (arriba izquierda)
    glLoadIdentity()
    glTranslatef(-2, 2, -8)
    glRotatef(angle, 1, 1, 0)
    cube()

    # Cubo 2 (arriba derecha)
    glLoadIdentity()
    glTranslatef(2, 2, -8)
    glRotatef(angle, 1, 0, 1)
    cube()

    # Cubo 3 (abajo izquierda)
    glLoadIdentity()
    glTranslatef(-2, -2, -8)
    glRotatef(angle, 0, 1, 1)
    cube()

    # Cubo 4 (abajo derecha)
    glLoadIdentity()
    glTranslatef(2, -2, -8)
    glRotatef(angle, 1, 1, 1)
    cube()

    glfw.swap_buffers(window)

    # Rotación
    angle += 0.01

def main():
    global window

    if not glfw.init():
        sys.exit()

    width, height = 500, 500
    window = glfw.create_window(width, height, "4 Cubos Rotando", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    glViewport(0, 0, width, height)
    init()

    while not glfw.window_should_close(window):
        draw_scene()
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()

    #Si necesitas ayuda con otra cosa, solo pidelo estoy feliz de ayudar