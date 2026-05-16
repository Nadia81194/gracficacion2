import cv2
import numpy as np
import math

WIDTH, HEIGHT = 800, 600
FPS = 30
DURATION_SEC = 60
TOTAL_FRAMES = FPS * DURATION_SEC
OUT_FILENAME = "demo_psicodelica.mp4"

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUT_FILENAME, fourcc, FPS, (WIDTH, HEIGHT))

def get_lissajous(t, num_points=200):
    # 1. Curva de Lissajous
    theta = np.linspace(0, 2 * np.pi, num_points)
    x = np.sin(3 * theta + t) * 150 + WIDTH // 2
    y = np.cos(2 * theta) * 150 + HEIGHT // 2
    return np.int32(np.column_stack((x, y)))

def get_spiral(t, num_points=300):
    # 2. Espiral de Arquímedes 
    theta = np.linspace(0, 8 * np.pi, num_points)
    r = (theta * 8) + (sin_t(t, 2) * 30)
    x = r * np.cos(theta + t) + WIDTH // 2
    y = r * np.sin(theta + t) + HEIGHT // 2
    return np.int32(np.column_stack((x, y)))

def get_polar_rose(t, num_points=250):
    # 3. Rosa 
    theta = np.linspace(0, 2 * np.pi, num_points)
    r = 180 * np.sin(5 * theta + t)
    x = r * np.cos(theta) + WIDTH // 2
    y = r * np.sin(theta) + HEIGHT // 2
    return np.int32(np.column_stack((x, y)))

def get_lemniscata(t, num_points=200):
    # 4. Lemniscata de Bernoulli
    theta = np.linspace(-np.pi/4, np.pi/4, num_points // 2)
    theta = np.concatenate([theta, theta + np.pi])
    r = 200 * np.sqrt(np.abs(np.cos(2 * theta))) * (1.0 + 0.2 * np.sin(t))
    x = r * np.cos(theta) + WIDTH // 2
    y = r * np.sin(theta) + HEIGHT // 2
    return np.int32(np.column_stack((x, y)))

def get_hypotrochoid(t, num_points=250):
    # 5. Hipotrocóide
    R, r, d = 150, 60, 40
    theta = np.linspace(0, 10 * np.pi, num_points)
    x = (R - r) * np.cos(theta) + d * np.cos((R - r) * theta / r + t) + WIDTH // 2
    y = (R - r) * np.sin(theta) - d * np.sin((R - r) * theta / r + t) + HEIGHT // 2
    return np.int32(np.column_stack((x, y)))

def get_cardioid(t, num_points=200):
    # 6. Cardioide rotatoria
    theta = np.linspace(0, 2 * np.pi, num_points)
    r = 100 * (1 - np.sin(theta + t))
    x = r * np.cos(theta) + WIDTH // 2
    y = r * np.sin(theta) + HEIGHT // 2
    return np.int32(np.column_stack((x, y)))

def sin_t(t, speed=1.0):
    return math.sin(t * speed)

def cos_t(t, speed=1.0):
    return math.cos(t * speed)


vignette_mask = np.zeros((HEIGHT, WIDTH), dtype=np.float32)
for i in range(HEIGHT):
    for j in range(WIDTH):
        # Distancia 
        dx = (j - WIDTH/2) / (WIDTH/2)
        dy = (i - HEIGHT/2) / (HEIGHT/2)
        dist = math.sqrt(dx*dx + dy*dy)
        vignette_mask[i, j] = np.clip(1.0 - dist * 0.7, 0.0, 1.0)

def apply_vignette(img):
    return (img * vignette_mask[:, :, np.newaxis]).astype(np.uint8)


print(f"Generando video '{OUT_FILENAME}' ({TOTAL_FRAMES} frames a 30 FPS)...")

for frame_idx in range(TOTAL_FRAMES):
    t = frame_idx / FPS  
    scene = int(t / 10)  
    local_t = t % 10.0
    frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    
    if scene == 0:
        # SEMAFOROS 
        num_circulos = 5
        for i in range(num_circulos):
            cx = int((i + 0.5) * (WIDTH / num_circulos))
            cy = int(HEIGHT // 2 + sin_t(t * 3 + i) * 60)
            
            # Color 
            r = int((sin_t(t * 5 + i) * 0.5 + 0.5) * 255)
            g = int((cos_t(t * 4 + i) * 0.5 + 0.5) * 255)
            b = int((sin_t(t * 3 + i) * 0.5 + 0.5) * 255)
            
            # Parpadeo 
            if sin_t(t * 15 + i) > 0:
                cv2.circle(frame, (cx, cy), 50, (b, g, r), -1)
                cv2.circle(frame, (cx, cy), 60, (255, 255, 255), 3)

    elif scene == 1:
        #  EL CUBO ROTATORIO E EPILÉPTICO
        cube_canvas = np.zeros_like(frame)
        sz = 120
        pts = np.array([[-sz, -sz], [sz, -sz], [sz, sz], [-sz, sz]], dtype=np.int32)
        pts_offset = pts + np.array([WIDTH // 2, HEIGHT // 2])
        
        # Color 
        col_r = int((sin_t(t * 4) * 0.5 + 0.5) * 255)
        col_g = int((cos_t(t * 3) * 0.5 + 0.5) * 255)
        col_b = int((sin_t(t * 5) * 0.5 + 0.5) * 255)
        
        cv2.fillPoly(cube_canvas, [pts_offset], (col_b, col_g, col_r))
        angle = t * 120  
        scale = 1.0 + sin_t(t * 5) * 0.3
        M = cv2.getRotationMatrix2D((WIDTH // 2, HEIGHT // 2), angle, scale)
        cube_transformed = cv2.warpAffine(cube_canvas, M, (WIDTH, HEIGHT))
        if sin_t(t * 40) > 0:
            frame[:, :] = (255 - col_b, 255 - col_g, 255 - col_r)
            frame = cv2.addWeighted(frame, 0.4, cube_transformed, 0.6, 0)
        else:
            frame = cube_transformed

    elif scene == 2:
        pts_lissa = get_lissajous(t)
        pts_spiral = get_spiral(t)
        
        cv2.polylines(frame, [pts_lissa], isClosed=True, color=(255, 0, 128), thickness=4)
        cv2.polylines(frame, [pts_spiral], isClosed=False, color=(0, 255, 128), thickness=3)
        cv2.circle(frame, (WIDTH // 2, HEIGHT // 2), int(100 + sin_t(t * 5) * 20), (255, 255, 255), 2)

    elif scene == 3:
        # EL TÚNEL GEOMÉTRICO 
        pts_rose = get_polar_rose(t)
        pts_lemni = get_lemniscata(t)
        cv2.polylines(frame, [pts_rose], isClosed=True, color=(128, 0, 255), thickness=3)
        cv2.polylines(frame, [pts_lemni], isClosed=True, color=(0, 255, 255), thickness=4)
        cv2.ellipse(frame, (WIDTH // 2, HEIGHT // 2), (200, 100), t * 50, 0, 360, (255, 128, 0), 3)

    elif scene == 4:
        # KALEIDOSCOPIO 
        pts_hypo = get_hypotrochoid(t)
        pts_card = get_cardioid(t)
        layer_curvas = np.zeros_like(frame)
        cv2.polylines(layer_curvas, [pts_hypo], isClosed=True, color=(255, 255, 0), thickness=3)
        cv2.polylines(layer_curvas, [pts_card], isClosed=True, color=(255, 0, 255), thickness=3)
        cv2.line(frame, (0, 0), (WIDTH, HEIGHT), (50, 50, 50), 2)
        cv2.line(frame, (WIDTH, 0), (0, HEIGHT), (50, 50, 50), 2)

        frame = cv2.addWeighted(frame, 0.3, layer_curvas, 0.7, 0)

    else:
        #FINAL + LOGO/TEXTO
        flash_idx = int(t * 12) % 3
        if flash_idx == 0:
            frame[:, :] = (0, 0, 150)  
        elif flash_idx == 1:
            frame[:, :] = (0, 150, 0)  
        else:
            frame[:, :] = (150, 0, 0)  

        barrido_y = int((t * 200) % HEIGHT)
        cv2.line(frame, (0, barrido_y), (WIDTH, barrido_y), (255, 255, 255), 5)
        cv2.putText(frame, "INSTITUTO TECNOLOGICO DE MORELIA", (50, HEIGHT // 2 - 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3, cv2.LINE_AA)
        cv2.putText(frame, "GRAFICACION - DEMO 64KB- NADIA CORIA ", (70, HEIGHT // 2 + 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)

    shift_pixels = int(5 * sin_t(t * 10))
    if abs(shift_pixels) > 0:
        b_channel, g_channel, r_channel = cv2.split(frame)
        r_channel = np.roll(r_channel, shift_pixels, axis=1)
        b_channel = np.roll(b_channel, -shift_pixels, axis=1)
        frame = cv2.merge([b_channel, g_channel, r_channel])
        

    frame = apply_vignette(frame)
    out.write(frame)


out.release()
print(f"VIDEO COMPLETO '{OUT_FILENAME}'")