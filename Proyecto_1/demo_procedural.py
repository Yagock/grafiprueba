import time, math
import numpy as np
import cv2

W, H = 800, 600
FPS = 30
DURATION = 56.0
TOTAL_SCENES = 8
BLOCK_DUR = DURATION / TOTAL_SCENES
TRANS_DUR = 1.5          # duración de cada transición

def clamp01(x): return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)
def smoothstep(a, b, x):
    x = clamp01((x - a) / (b - a))
    return x * x * (3 - 2 * x)

def poly_param(fx, fy, t0, t1, n, cx, cy, sx, sy):
    ts = np.linspace(t0, t1, n, dtype=np.float32)
    xs = fx(ts) * sx + cx
    ys = fy(ts) * sy + cy
    return np.round(np.stack([xs, ys], 1)).astype(np.int32).reshape((-1, 1, 2))

def hsv_to_bgr(h, s, v):
    hsv = np.uint8([[[int(h) % 180, int(np.clip(s, 0, 255)), int(np.clip(v, 0, 255))]]])
    return tuple(int(x) for x in cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)[0, 0])

def background_hsv_gradient(img, t, hue0=10, hue1=140):
    hsv = np.zeros((H, W, 3), np.uint8)
    ys = np.linspace(0, 1, H, dtype=np.float32)
    hue = (hue0 + (hue1 - hue0) * ys + 10 * np.sin(t * 0.4 + ys * 2.0)).astype(np.float32)
    hsv[:, :, 0] = np.clip(hue, 0, 179).astype(np.uint8)[:, None]
    hsv[:, :, 1] = 200
    hsv[:, :, 2] = (40 + 120 * (1 - ys)).astype(np.uint8)[:, None]
    img[:] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def post_vignette(img, strength=0.7):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx = (xx - W * 0.5) / (W * 0.5)
    ny = (yy - H * 0.5) / (H * 0.5)
    r2 = nx * nx + ny * ny
    mask = np.clip(1.0 - strength * r2, 0.0, 1.0)
    return (img.astype(np.float32) * mask[..., None]).astype(np.uint8)

def post_scanlines(img, strength=0.15):
    out = img.astype(np.float32)
    y = np.arange(H, dtype=np.float32)
    m = 1.0 - strength * (0.5 + 0.5 * np.sin(2 * np.pi * y / 3.0))
    out *= m[:, None, None]
    return np.clip(out, 0, 255).astype(np.uint8)

# ESCENAS

# Primer escena - Intro
def scene_credits(img, t):
    background_hsv_gradient(img, t, hue0=110, hue1=150)
    cv2.circle(img, (W // 2, H // 2), 180, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.ellipse(img, (W // 2, H // 2), (220, 140), t * 30, 0, 360, (200, 255, 255), 1, cv2.LINE_AA)
    oy = int(math.sin(t * 1.5) * 12)
    cv2.putText(img, "PROYECTO FINAL: DEMO PROCEDURAL", (75, 230 + oy),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3, cv2.LINE_AA)
    cv2.putText(img, "Diego Santiago Zavala Urueta", (75, 285 + oy),
                cv2.FONT_HERSHEY_SIMPLEX, 0.85, (200, 220, 255), 2, cv2.LINE_AA)
    cv2.putText(img, "Ingenieria en Sistemas Computacionales", (75, 325 + oy),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (180, 200, 230), 2, cv2.LINE_AA)
    cv2.putText(img, "Proyecto 1", (75, 375 + oy),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 200), 2, cv2.LINE_AA)

# Segunda escena - Lemniscata de Bernoulli (rotación + pulso de escala)
def scene_lemniscate(img, t):
    background_hsv_gradient(img, t, hue0=160, hue1=10)
    fx = lambda ts: np.sin(ts)
    fy = lambda ts: np.sin(ts) * np.cos(ts)
    pts = poly_param(fx, fy, 0, 2 * math.pi, 600, W * 0.5, H * 0.5, 280, 280)
    temp = np.zeros_like(img)
    cv2.polylines(temp, [pts], True, hsv_to_bgr(int(t * 20), 220, 255), 3, cv2.LINE_AA)
    M = cv2.getRotationMatrix2D((W / 2, H / 2), t * 40, 1.0 + 0.2 * math.sin(t * 2))
    cv2.addWeighted(img, 1.0, cv2.warpAffine(temp, M, (W, H)), 1.0, 0, img)

# Tercera escena - Espiral de Arquímedes  (rotación + shear)
def scene_spiral(img, t):
    background_hsv_gradient(img, t, hue0=20, hue1=50)
    t_local = t % BLOCK_DUR
    fx = lambda ts: ts * np.cos(ts)
    fy = lambda ts: ts * np.sin(ts)
    pts = poly_param(fx, fy, 0, max(0.1, t_local * 5), 500, W * 0.5, H * 0.5, 12, 12)
    temp = np.zeros_like(img)
    cv2.polylines(temp, [pts], False, hsv_to_bgr(40, 200, 255), 2, cv2.LINE_AA)
    M_rot = cv2.getRotationMatrix2D((W / 2, H / 2), t * 60, 1.0)
    rotated = cv2.warpAffine(temp, M_rot, (W, H))
    M_shear = np.float32([[1, 0.3 * math.sin(t * 2), 0], [0, 1, 0]])
    cv2.addWeighted(img, 1.0, cv2.warpAffine(rotated, M_shear, (W, H)), 1.0, 0, img)

# Cuarta escena - Rosa Polar  (rotación simple)
def scene_polar_rose(img, t):
    background_hsv_gradient(img, t, hue0=130, hue1=170)
    fx = lambda ts: np.cos(4 * ts) * np.cos(ts)
    fy = lambda ts: np.cos(4 * ts) * np.sin(ts)
    pts = poly_param(fx, fy, 0, 2 * math.pi, 800, W * 0.5, H * 0.5, 220, 220)
    temp = np.zeros_like(img)
    cv2.polylines(temp, [pts], True, hsv_to_bgr(140, 220, 255), 3, cv2.LINE_AA)
    M = cv2.getRotationMatrix2D((W / 2, H / 2), -t * 50, 1.0)
    cv2.addWeighted(img, 1.0, cv2.warpAffine(temp, M, (W, H)), 1.0, 0, img)

# Quinta escena - Lissajous  (rotación + espejo)
def scene_lissajous(img, t):
    background_hsv_gradient(img, t, hue0=60, hue1=90)
    fx = lambda ts: np.sin(3 * ts)
    fy = lambda ts: np.sin(2 * ts)
    pts = poly_param(fx, fy, 0, 2 * math.pi, 600, W * 0.35, H * 0.5, 150, 150)
    temp = np.zeros_like(img)
    cv2.polylines(temp, [pts], True, hsv_to_bgr(75, 230, 255), 2, cv2.LINE_AA)
    M_rot = cv2.getRotationMatrix2D((W * 0.35, H * 0.5), t * 45, 1.0)
    rotated = cv2.warpAffine(temp, M_rot, (W, H))
    M_mirror = np.float32([[-1, 0, W], [0, 1, 0]])
    mirrored = cv2.warpAffine(rotated, M_mirror, (W, H))
    cv2.addWeighted(img, 1.0, rotated, 1.0, 0, img)
    cv2.addWeighted(img, 1.0, mirrored, 1.0, 0, img)

# Sexta escena - Cardioide  (rotación + fillPoly)
def scene_cardioid(img, t):
    background_hsv_gradient(img, t, hue0=100, hue1=130)
    r = lambda ts: 1.0 - np.cos(ts)
    fx = lambda ts: r(ts) * np.cos(ts)
    fy = lambda ts: r(ts) * np.sin(ts)
    pts = poly_param(fx, fy, 0, 2 * math.pi, 500, W * 0.5, H * 0.5, 120, 120)
    temp = np.zeros_like(img)
    cv2.fillPoly(temp, [pts], (40, 80, 40))
    cv2.polylines(temp, [pts], True, hsv_to_bgr(115, 240, 255), 3, cv2.LINE_AA)
    M = cv2.getRotationMatrix2D((W / 2, H / 2), t * 70, 1.0)
    cv2.addWeighted(img, 1.0, cv2.warpAffine(temp, M, (W, H)), 1.0, 0, img)

# Séptima escena - Astroide  (rotación + ejes decorativos)
def scene_astroid(img, t):
    background_hsv_gradient(img, t, hue0=0, hue1=30)
    fx = lambda ts: np.power(np.cos(ts), 3)
    fy = lambda ts: np.power(np.sin(ts), 3)
    pts = poly_param(fx, fy, 0, 2 * math.pi, 600, W * 0.5, H * 0.5, 220, 220)
    temp = np.zeros_like(img)
    cv2.line(temp, (W // 2, H // 2 - 250), (W // 2, H // 2 + 250), (255, 255, 255), 1, cv2.LINE_AA)
    cv2.line(temp, (W // 2 - 250, H // 2), (W // 2 + 250, H // 2), (255, 255, 255), 1, cv2.LINE_AA)
    cv2.polylines(temp, [pts], True, hsv_to_bgr(15, 220, 255), 3, cv2.LINE_AA)
    M = cv2.getRotationMatrix2D((W / 2, H / 2), -t * 50, 1.0)
    cv2.addWeighted(img, 1.0, cv2.warpAffine(temp, M, (W, H)), 1.0, 0, img)

# Octava escena - Despedida / Outro
def scene_outro(img, t):
    # Fondo negro sólido
    img[:] = 0

    # Anillos que se expanden y desvanecen (onda de choque)
    for i in range(3):
        phase = (t * 0.6 + i * 0.33) % 1.0
        r = int(phase * 350)
        alpha = 1.0 - phase
        col = hsv_to_bgr(int(150 + i * 12), 180, int(200 * alpha))
        cv2.circle(img, (W // 2, H // 2), max(1, r), col, 2, cv2.LINE_AA)

    pulse = 1.0 + 0.03 * math.sin(t * 2.5)
    scale = 4.5 * pulse
    thickness = 10
    text = "FIN"
    (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, scale, thickness)
    tx = (W - tw) // 2
    ty = (H + th) // 2
    cv2.putText(img, text, (tx + 6, ty + 6),
                cv2.FONT_HERSHEY_SIMPLEX, scale, (0, 60, 80), thickness + 4, cv2.LINE_AA)
    cv2.putText(img, text, (tx, ty),
                cv2.FONT_HERSHEY_SIMPLEX, scale, (255, 255, 255), thickness, cv2.LINE_AA)

def render_scene(buf, scene_id, t):
    if   scene_id == 0: scene_credits(buf, t)
    elif scene_id == 1: scene_lemniscate(buf, t)
    elif scene_id == 2: scene_spiral(buf, t)
    elif scene_id == 3: scene_polar_rose(buf, t)
    elif scene_id == 4: scene_lissajous(buf, t)
    elif scene_id == 5: scene_cardioid(buf, t)
    elif scene_id == 6: scene_astroid(buf, t)
    else:               scene_outro(buf, t)

# Transiciones
# 1→2  Fade suave (crossfade)
# 2→3  Flash blanco
# 3→4  Barrido izquierda→derecha
# 4→5  Fade suave
# 5→6  Flash blanco
# 6→7  Barrido derecha→izquierda
# 7→8  Fade suave (fade a negro → fade desde negro)

def apply_transition(bufA, bufB, a, trans_type, img_w, img_h):
    """
    Mezcla bufA (escena actual) con bufB (siguiente) usando el tipo indicado.
    a: progreso de la transición [0..1]
    trans_type: 0=fade, 1=flash, 2=wipe_ltr, 3=wipe_rtl
    """
    if trans_type == 0:
        return cv2.addWeighted(bufA, 1.0 - a, bufB, a, 0)

    elif trans_type == 1:
        mixed = cv2.addWeighted(bufA, 1.0 - a, bufB, a, 0)
        flash = math.sin(a * math.pi)
        white = np.full_like(mixed, 255)
        return cv2.addWeighted(mixed, 1.0, white, 0.6 * flash, 0)

    elif trans_type == 2:
        out = bufA.copy()
        cut = int(a * img_w)
        if cut > 0:
            out[:, :cut] = bufB[:, :cut]
        return out

    elif trans_type == 3:
        out = bufA.copy()
        cut = int((1.0 - a) * img_w)
        if cut < img_w:
            out[:, cut:] = bufB[:, cut:]
        return out

    return cv2.addWeighted(bufA, 1.0 - a, bufB, a, 0)

TRANS_TYPE = [0, 1, 2, 0, 1, 3, 0]

# TIMELINE

def timeline(t, bufA, bufB):
    block   = int(min(TOTAL_SCENES - 1, max(0, t // BLOCK_DUR)))
    t_in    = t - block * BLOCK_DUR

    render_scene(bufA, block, t)
    frame = bufA

    trans_start = BLOCK_DUR - TRANS_DUR

    if block < TOTAL_SCENES - 1 and t_in >= trans_start:
        render_scene(bufB, block + 1, t)
        a = smoothstep(trans_start, BLOCK_DUR, t_in)
        tt = TRANS_TYPE[block] if block < len(TRANS_TYPE) else 0
        frame = apply_transition(bufA, bufB, a, tt, W, H)

    # Fade in al inicio y fade out al final del video
    fin  = smoothstep(0.0, 1.5, t)
    fout = 1.0 - smoothstep(DURATION - 1.5, DURATION, t)
    f = fin * fout
    if f < 0.999:
        frame = (frame.astype(np.float32) * f).astype(np.uint8)

    return frame

# MAIN

def main():
    bufA = np.zeros((H, W, 3), np.uint8)
    bufB = np.zeros((H, W, 3), np.uint8)

    fourcc    = cv2.VideoWriter_fourcc(*'mp4v')
    out_video = cv2.VideoWriter('demo_procedural.mp4', fourcc, FPS, (W, H))

    total_frames = int(DURATION * FPS)
    print("Iniciando render y exportacion. Por favor espera...")

    for i in range(total_frames):
        t     = i / FPS
        frame = timeline(t, bufA, bufB)
        frame = post_vignette(frame, 0.7)
        frame = post_scanlines(frame, 0.14)

        out_video.write(frame)
        cv2.imshow("Proyecto Final: Demo Procedural (OpenCV)", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    out_video.release()
    print("Video exportado con exito como 'demo_procedural.mp4'")
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()