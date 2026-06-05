import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

rotation = 0.0

def draw_sphere(radius, slices=30, stacks=30):
    """Dibuja una esfera con normales suaves para iluminación correcta (Misión 2)"""
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)  # Misión 2: normales para iluminación suave
    gluSphere(quad, radius, slices, stacks)
    gluDeleteQuadric(quad)

def set_material(ambient, diffuse, specular, shininess, face=GL_FRONT):
    """Aplica material a la esfera actual (Misión 3)"""
    glMaterialfv(face, GL_AMBIENT,   ambient)
    glMaterialfv(face, GL_DIFFUSE,   diffuse)
    glMaterialfv(face, GL_SPECULAR,  specular)
    glMaterialf (face, GL_SHININESS, shininess)

def draw_eye():
    glPushMatrix()

    # Piel/rojizo — difuso cálido, especular suave
    set_material(
        ambient   = [0.3,  0.15, 0.1,  1.0],
        diffuse   = [0.85, 0.67, 0.65, 1.0],
        specular  = [0.3,  0.2,  0.2,  1.0],
        shininess = 20
    )
    glPushMatrix()
    glTranslatef(0.7, 0, 0)
    draw_sphere(0.54)
    glPopMatrix()

    # Esclerótica (blanco) — especular moderado, shininess alto
    set_material(
        ambient   = [0.4,  0.4,  0.4,  1.0],
        diffuse   = [1.0,  1.0,  1.0,  1.0],
        specular  = [0.8,  0.8,  0.8,  1.0],
        shininess = 80
    )
    glPushMatrix()
    glTranslatef(0.56, 0, 0)
    draw_sphere(0.6)
    glPopMatrix()

    # Iris (azul claro) — especular bajo, shininess medio
    set_material(
        ambient   = [0.2,  0.2,  0.3,  1.0],
        diffuse   = [0.84, 0.85, 0.92, 1.0],
        specular  = [0.3,  0.3,  0.4,  1.0],
        shininess = 32
    )
    glPushMatrix()
    glTranslatef(0.49, 0, 0)
    draw_sphere(0.55)
    glPopMatrix()

    # Pupila (negro) — casi sin especular, shininess bajo
    set_material(
        ambient   = [0.02, 0.02, 0.02, 1.0],
        diffuse   = [0.05, 0.05, 0.05, 1.0],
        specular  = [0.05, 0.05, 0.05, 1.0],
        shininess = 8
    )
    glPushMatrix()
    glTranslatef(0.3, 0, 0)
    draw_sphere(0.4)
    glPopMatrix()

    glPopMatrix()

def setup_lighting():
    """Configura iluminación principal + luz de relleno (Misiones 1 y Bonus)"""

    # ── Misión 1: Luz principal (GL_LIGHT0) ──────────────────────────────────
    glLightfv(GL_LIGHT0, GL_AMBIENT,  [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    # ── Bonus: Luz de relleno (GL_LIGHT1) — tono azul tenue ──────────────────
    glLightfv(GL_LIGHT1, GL_AMBIENT,  [0.0, 0.0, 0.05, 1.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE,  [0.1, 0.1, 0.3,  1.0])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [0.1, 0.1, 0.2,  1.0])

    glEnable(GL_LIGHT1)

def main():
    global rotation

    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Ojo 3D - Iluminación y Materiales", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # ── Misión 1: Activar estados de iluminación ─────────────────────────────
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glClearColor(0.54, 0.72, 0.84, 1.0)
    setup_lighting()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800/600, 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -5)

        # ── Misión 5: Luz fija en el mundo (antes de rotar el objeto) ─────────
        glLightfv(GL_LIGHT0, GL_POSITION, [2.0,  2.0, 2.0, 1.0])
        glLightfv(GL_LIGHT1, GL_POSITION, [-2.0, 1.0, 1.0, 1.0])

        rotation += 0.05
        glRotatef(rotation, 0, 1, 0)

        draw_eye()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()


# =============================================================================
# PREGUNTAS DE REFLEXIÓN
# =============================================================================

# Misión 5: ¿Por qué la luz cambia cuando rota?
# ─────────────────────────────────────────────
# En OpenGL la posición de la luz se transforma con la matriz MODELVIEW que
# esté activa en el momento en que se llama glLightfv(..., GL_POSITION, ...).
# Si la llamada ocurre ANTES de glRotatef (Opción A), la luz queda fija en el
# mundo y el objeto rota bajo ella — las sombras cambian con la rotación.
# Si la llamada ocurre DESPUÉS de glRotatef (Opción B), la luz rota junto con
# el objeto y la iluminación siempre se ve igual sin importar el ángulo.
# En este script se usó la Opción A: la luz es fija en el mundo.