#!/usr/bin/env python3
"""
Operación Órbita Dual — ejemplo funcional (GLFW + PyOpenGL, pipeline fijo).
Sin GLUT: la esfera se dibuja con gluSphere (GLU).

Controles:
  1  Modo: rotar OBJETO (cámara fija)
  2  Modo: orbitar CÁMARA (objeto fijo, variante rotate(-a) + translate)
  3  Modo: gluLookAt (órbita del ojo)
  ESC o Q  Salir
"""

from __future__ import annotations

import math
import sys

import glfw
from OpenGL.GL import *
from OpenGL.GLU import (
    GLU_FILL,
    gluLookAt,
    gluNewQuadric,
    gluPerspective,
    gluQuadricDrawStyle,
    gluQuadricNormals,
    GLU_SMOOTH,
    gluSphere,
)

# ---------------------------------------------------------------------------
# Configuración
# CAM_DISTANCE: distancia de la cámara al origen. Mayor = objeto más pequeño.
# ORBIT_RADIUS: radio de la órbita en gluLookAt (Modo 3). Mayor = más lejos.
# ANGLE_SPEED:  grados por frame. Mayor = rotación más rápida.
# ---------------------------------------------------------------------------
WINDOW_TITLE  = "Orbita Dual (GLFW) — 1/2/3 cambia modo"
INITIAL_MODE  = 1
ORBIT_RADIUS  = 5.0   # radio de órbita en Modo 3
CAM_DISTANCE  = 5.0   # alejamiento en -Z en Modos 1 y 2
ANGLE_SPEED   = 0.6   # velocidad de rotación en grados/frame

USE_LIGHTING  = True  # Misión 3: iluminación activa

# ---------------------------------------------------------------------------
# Geometría
# ---------------------------------------------------------------------------
_quadric = None

def draw_sphere(radius: float = 1.0) -> None:
    global _quadric
    if _quadric is None:
        _quadric = gluNewQuadric()
        gluQuadricDrawStyle(_quadric, GLU_FILL)
        gluQuadricNormals(_quadric, GLU_SMOOTH)  # normales para iluminación suave
    gluSphere(_quadric, radius, 40, 24)


def setup_basic_lighting() -> None:
    """
    Luz posicional fija en coordenadas de mundo.
    Al definirla ANTES de cualquier rotación del objeto, la luz no se mueve
    con él — las sombras cambian al rotar, lo que da sensación de volumen real.
    """
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glLightfv(GL_LIGHT0, GL_AMBIENT,  [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [0.9, 0.9, 0.85, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0,  1.0])
    # w=1.0 → luz posicional; posición fija en el mundo (se llama antes de rotar)
    glLightfv(GL_LIGHT0, GL_POSITION, [3.0, 3.0, 3.0, 1.0])

    glMaterialf(GL_FRONT, GL_SHININESS, 64)
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.8, 0.8, 0.8, 1.0])

    # Luz de relleno tenue (azul) para que el lado oscuro no quede negro total
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_AMBIENT,  [0.0, 0.0, 0.05, 1.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE,  [0.1, 0.1, 0.3,  1.0])
    glLightfv(GL_LIGHT1, GL_POSITION, [-3.0, 1.0, 1.0, 1.0])


# ---------------------------------------------------------------------------
# Modos de cámara / objeto
# ---------------------------------------------------------------------------
def render_rotating_object(angle: float) -> None:
    """Modo 1: cámara fija (translate -Z), el objeto rota."""
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -CAM_DISTANCE)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glColor3f(0.35, 0.65, 1.0)
    draw_sphere(1.0)


def render_orbiting_camera(angle: float) -> None:
    """
    Modo 2: primero rotar la vista (-angle), luego alejar en -Z.
    El objeto queda conceptualmente fijo en el origen.
    Orden: rotate(-a) → translate(-Z)
    """
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(-angle, 0.0, 1.0, 0.0)
    glTranslatef(0.0, 0.0, -CAM_DISTANCE)
    glColor3f(1.0, 0.55, 0.35)
    draw_sphere(1.0)


def render_orbiting_camera_variant_b(angle: float) -> None:
    """
    Variante B: translate(-Z) primero, luego rotate(+angle).
    Comparado con render_orbiting_camera, el objeto aparenta girar
    (igual que Modo 1) porque el orden invierte la semántica.
    """
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -CAM_DISTANCE)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glColor3f(0.45, 1.0, 0.45)
    draw_sphere(1.0)


def render_with_lookat(angle: float) -> None:
    """Modo 3: cámara en órbita con gluLookAt."""
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    a = math.radians(angle)
    cam_x = ORBIT_RADIUS * math.sin(a)
    cam_z = ORBIT_RADIUS * math.cos(a)
    gluLookAt(cam_x, 0.0, cam_z,   # posición del ojo
              0.0,   0.0, 0.0,     # objetivo (origen)
              0.0,   1.0, 0.0)     # vector "arriba"
    glColor3f(0.95, 0.85, 0.35)
    draw_sphere(1.0)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    if not glfw.init():
        print("Error: no se pudo inicializar GLFW", file=sys.stderr)
        sys.exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)

    window = glfw.create_window(800, 600, WINDOW_TITLE, None, None)
    if not window:
        glfw.terminate()
        sys.exit(1)

    glfw.make_context_current(window)
    glfw.swap_interval(1)

    mode = INITIAL_MODE

    def on_key(win, key, scancode, action, mods):
        nonlocal mode
        if action != glfw.PRESS:
            return
        if key in (glfw.KEY_ESCAPE, glfw.KEY_Q):
            glfw.set_window_should_close(win, True)
        elif key == glfw.KEY_1:
            mode = 1
        elif key == glfw.KEY_2:
            mode = 2
        elif key == glfw.KEY_3:
            mode = 3

    glfw.set_key_callback(window, on_key)

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.08, 0.08, 0.12, 1.0)

    if USE_LIGHTING:
        setup_basic_lighting()

    angle = 0.0

    while not glfw.window_should_close(window):
        fb_w, fb_h = glfw.get_framebuffer_size(window)
        if fb_h <= 0:
            fb_h = 1
        glViewport(0, 0, fb_w, fb_h)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(50.0, fb_w / float(fb_h), 0.1, 100.0)

        if mode == 1:
            render_rotating_object(angle)
        elif mode == 2:
            render_orbiting_camera(angle)
        else:
            render_with_lookat(angle)

        angle += ANGLE_SPEED
        if angle >= 360.0:
            angle -= 360.0

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()