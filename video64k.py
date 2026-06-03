import time
import math
import numpy as np
import cv2
from datetime import datetime
W, H = 800, 600
FPS = 30
DURATION = 60.0  
SAVE_TO_FILE = True  

def clamp01(x): 
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)

def smoothstep(a, b, x):
    x = clamp01((x - a) / (b - a))
    return x * x * (3 - 2 * x)

def poly_param(fx, fy, t0, t1, n, cx, cy, sx, sy):
    ts = np.linspace(t0, t1, n, dtype=np.float32)
    xs = fx(ts) * sx + cx
    ys = fy(ts) * sy + cy
    return np.round(np.stack([xs, ys], 1)).astype(np.int32).reshape((-1, 1, 2))

def hsv_to_bgr(h, s, v):
    hsv = np.uint8([[[h % 180, np.clip(s, 0, 255), np.clip(v, 0, 255)]]])
    return tuple(int(x) for x in cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)[0, 0])

# FONDOS (MÁS CHIDOS Y PSICODÉLICOS muejejeje) ---

def background_hsv_gradient(img, t, hue0=10, hue1=140):
    """Tu degradado original modificado para que los colores roten salvajemente"""
    hsv = np.zeros((H, W, 3), np.uint8)
    ys = np.linspace(0, 1, H, dtype=np.float32)
    color_shift = t * 45 
    hue = (hue0 + color_shift + (hue1 - hue0) * ys + 30 * np.sin(t * 1.5 + ys * 3.0)).astype(np.float32)
    
    hsv[:, :, 0] = np.clip(hue % 180, 0, 179).astype(np.uint8)[:, None]
    hsv[:, :, 1] = int(220 + 35 * math.sin(t * 4))
    hsv[:, :, 2] = (50 + 150 * (1 - ys)).astype(np.uint8)[:, None]
    img[:] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


def scene_0_intro(img, t):
    """PORTADA DINÁMICA OBLIGATORIA CON TUS DATOS"""
    background_hsv_gradient(img, t, hue0=130, hue1=170)
    rng = np.random.default_rng(1)
    xs = rng.integers(0, W, 400)
    ys = rng.integers(0, int(H * 0.8), 400)
    xs = (xs + int(t * 80)) % W
    img[ys, xs] = (255, 255, 255)
    cv2.rectangle(img, (40, 60), (W-40, H-60), (15, 5, 25), -1)
    cv2.rectangle(img, (40, 60), (W-40, H-60), hsv_to_bgr(int(t*60), 255, 255), 3)

    # Efecto de rebote loco en el título
    bounce = int(12 * math.sin(t * 8))
    today_str = datetime.today().strftime('%d/%m/%Y')

    cv2.putText(img, "TECNM", (W//2 - 110, 140 + bounce), cv2.FONT_HERSHEY_TRIPLEX, 2.2, (0, 255, 255), 4, cv2.LINE_AA)
    cv2.putText(img, "GRAFICACION video 64K", (70, 230), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 255), 3, cv2.LINE_AA)
    cv2.putText(img, "ALUMNA: NADIA CORIA ARGON", (70, 310), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img, f"FECHA: {today_str}", (70, 390), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)
    
    # Decoración entretenida abajo
    cv2.putText(img, "PROYECTO PROCEDURAL", (70, 480), cv2.FONT_HERSHEY_PLAIN, 1.5, (200, 200, 200), 2, cv2.LINE_AA)
    if int(t * 3) % 2 == 0:
        cv2.putText(img, ">> LOADING SYSTEM <<", (W//2 - 140, 540), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2, cv2.LINE_AA)

def scene_1_lissajous(img, t):
    """Tu Lissajous original acelerado y con escala cambiante"""
    background_hsv_gradient(img, t, hue0=18, hue1=60)
    a = 3 + 1.2 * math.sin(t * 1.5)
    b = 2 + 1.2 * math.cos(t * 2.0)
    delta = math.pi/2 + 0.8 * math.sin(t * 1.2)
    
    fx = lambda x: np.sin(a * x + delta)
    fy = lambda x: np.sin(b * x)
    pulse = 260 + int(40 * math.sin(t * 10))
    pts = poly_param(fx, fy, 0, 2 * math.pi, 900, W * 0.5, H * 0.45, pulse, 180)
    
    col = hsv_to_bgr(int(t * 90), 255, 255) 
    cv2.polylines(img, [pts], False, col, 4, cv2.LINE_AA)
    cv2.putText(img, "ESCENA 1: LISSAJOUS", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2)

def scene_2_rose_polar(img, t):
    """Tu Rosa Polar original mutando velozmente"""
    background_hsv_gradient(img, t, hue0=120, hue1=165)
    
    k = 5 + int(2 * math.sin(t * 2)) 
    theta0 = t * 2.5 
    
    fx = lambda th: np.cos(k * th) * np.cos(th + theta0)
    fy = lambda th: np.cos(k * th) * np.sin(th + theta0)
    
    # Efecto deformador multiplicando las amplitudes por una onda seno
    scale_x = int(240 + 50 * math.cos(t * 4))
    pts = poly_param(fx, fy, 0, 2 * math.pi, 1200, W * 0.5, H * 0.45, scale_x, 240)
    
    col = hsv_to_bgr(int(145 + 90 * np.sin(t * 2.0)), 245, 255)
    cv2.polylines(img, [pts], False, col, 3, cv2.LINE_AA)
    
    # círculos Beats originales moviéndose de arriba a abajo
    for i in range(6):
        r = int(25 + 15 * np.sin(t * 6.0 + i))
        y_pos = int(H * 0.78 + 30 * math.cos(t * 4 + i))
        cv2.circle(img, (int(W * 0.18 + i * 110), y_pos), max(1, r), (255, 255, 255), 2, cv2.LINE_AA)
        
    cv2.putText(img, "ESCENA 2: ROSA POLAR MOD", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2)

def scene_3_spirograph(img, t):
    """Tu Espirógrafo original con líneas multiplicadas e invertidas"""
    background_hsv_gradient(img, t, hue0=80, hue1=20)
    
    R, r, d = 8.0, 3.0, 5.0
    w = (R - r) / r
    # Inyectamos más distorsión matemática en los senos interiores
    fx = lambda x: (R - r) * np.cos(x) + d * np.cos(w * x + 1.5 * np.sin(t * 2.0))
    fy = lambda x: (R - r) * np.sin(x) - d * np.sin(w * x + 1.5 * np.cos(t * 2.0))
    
    # Trazado gigante con rotación exagerada
    pts = poly_param(fx, fy, 0, 14 * math.pi, 1600, W * 0.5, H * 0.46, 32, 32)
    col = hsv_to_bgr(int(t * 120), 255, 255)
    cv2.polylines(img, [pts], False, col, 3, cv2.LINE_AA)
    
    # Dibujar un segundo espirógrafo espejo más chico flotando alrededor para rellenar
    pts_small = poly_param(fx, fy, 0, 14 * math.pi, 800, W * 0.5 + 100 * math.sin(t), H * 0.46, 12, 12)
    cv2.polylines(img, [pts_small], False, (255, 255, 255), 1, cv2.LINE_AA)
    
    cv2.putText(img, "ESCENA 3: ESPIROGRAFO LOCO", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2)

def scene_4_particles(img, t, rng):
    """Tus Partículas originales con ráfagas de velocidad y distorsión de viento"""
    background_hsv_gradient(img, t, hue0=150, hue1=100)
    n = 1500 # Aumentamos cantidad de partículas
    xs = rng.random(n) * W
    ys = rng.random(n) * H
    
    # Agitamos los coeficientes de distorsión para ráfagas mucho más caóticas e intermitentes
    wave_speed = 3.5
    xs = (xs + 180 * np.sin(ys / 40.0 + t * wave_speed) + 80 * np.cos(t * 2.0)) % W
    ys = (ys + 120 * np.cos(xs / 50.0 + t * wave_speed) + 60 * np.sin(t * 2.5)) % H
    
    v = (0.5 + 0.5 * np.sin(t * 4.0)).astype(float) if hasattr(t, "astype") else (0.5 + 0.5 * math.sin(t * 4.0))
    col = hsv_to_bgr(int(t * 50 % 180), 255, int(210 + 45 * v))
    
    # Dibujar como cuadros retro grandes en lugar de pixeles unitarios ocultos
    for x, y in zip(xs.astype(np.int32), ys.astype(np.int32)):
        if 0 <= x < W-2 and 0 <= y < H-2:
            img[y:y+2, x:x+2] = col
            
    cv2.putText(img, "ESCENA 4: TORMENTA DE PARTICULAS", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2)

def scene_5_fire(img, t, state):
    """Tu Fuego procedural original pero convertido en un infierno multicolor"""
    heat = state["heat"]
    rng = state["rng"]
    # Enfriamiento dinámico irregular para simular explosiones en la base
    heat[:] = (heat * (0.91 + 0.03 * math.sin(t*5))).astype(np.float32)

    base_n = 2000 # Más densidad de fuego
    xs = rng.integers(0, W, base_n)
    ys = rng.integers(int(H * 0.80), H, base_n)
    heat[ys, xs] += rng.random(base_n) * (1.0 + 0.8 * (0.5 + 0.5 * math.sin(t * 5.0)))

    heat[:] = cv2.GaussianBlur(heat, (0, 0), 3.0)
    heat[:-4, :] = heat[4:, :]  # Subida de fuego más veloz desplazando 4 pixeles
    heat[-4:, :] *= 0.0

    # Variamos el mapeo de color para que el fuego cambie de tonalidad mística verde/azul/rojo con el tiempo
    shift = int(t * 30) % 180
    h = ((20 + shift) - 30 * np.clip(heat, 0, 1)).astype(np.uint8)      
    s = (240 - 60 * np.clip(heat, 0, 1)).astype(np.uint8)     
    v = (40 + 215 * np.clip(heat, 0, 1)).astype(np.uint8)     
    
    hsv = np.dstack([h, s, v]).astype(np.uint8)
    img[:] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # Silueta de piso y chispas flotando por toda la pantalla
    cv2.rectangle(img, (0, int(H * 0.83)), (W, H), (5, 5, 5), -1)
    sparks = 250
    sx = rng.integers(0, W, sparks)
    sy = rng.integers(int(H * 0.2), int(H * 0.9), sparks) # Chispas suben más alto ahora
    # Animación lateral de chispas
    sx = (sx + int(t * 120)) % W
    img[sy, sx] = (255, 255, 255)
    
    cv2.putText(img, "ESCENA 5: INFIERNO PROCEDURAL", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2)


def render_scene(buf, scene_id, t, rng, fire_state):
    if scene_id == 0:
        scene_0_intro(buf, t)
    elif scene_id == 1:
        scene_1_lissajous(buf, t)
    elif scene_id == 2:
        scene_2_rose_polar(buf, t)
    elif scene_id == 3:
        scene_3_spirograph(buf, t)
    elif scene_id == 4:
        scene_4_particles(buf, t, rng)
    else:
        scene_5_fire(buf, t, fire_state)

def timeline(t, rng, bufA, bufB, fire_state):
    # Duración total = 60 segundos. 6 escenas -> 10 segundos clavados por bloque
    block = int(min(5, max(0, t // 10)))
    t_in = t - block * 10

    render_scene(bufA, block, t, rng, fire_state)
    frame = bufA.copy()

    # Transiciones rápidas e intensas (Últimos 1.2s de cada bloque)
    if block < 5 and t_in >= 8.8:
        render_scene(bufA, block, t, rng, fire_state)
        render_scene(bufB, block + 1, t, rng, fire_state)
        a = smoothstep(8.8, 10.0, t_in)
        
        # Efecto parpadeo/estrobo en cortes para aumentar dinamismo retro
        if int(t * 15) % 2 == 0:
            frame = cv2.addWeighted(bufA, 1.0 - a, bufB, a, 0)
        else:
            frame = bufB # Salto directo intermitente
            
        # Destello blanco veloz al cambiar
        flash = smoothstep(9.7, 10.0, t_in)
        if flash > 0:
            frame = cv2.addWeighted(frame, 1.0, np.full_like(frame, 255), 0.25 * flash, 0)

    # Fade out final en los últimos 2 segundos de la demo entera
    if t > DURATION - 2.0:
        fout = 1.0 - smoothstep(DURATION - 2.0, DURATION, t)
        frame = (frame.astype(np.float32) * fout).astype(np.uint8)
        
    return frame

# --- MOTOR PRINCIPAL ---

def main():
    rng = np.random.default_rng(2026)
    bufA = np.zeros((H, W, 3), np.uint8)
    bufB = np.zeros((H, W, 3), np.uint8)

    fire_state = {
        "heat": np.zeros((H, W), np.float32),
        "rng": np.random.default_rng(777),
    }

    total_frames = int(DURATION * FPS)
    
    # Configuración de render a mp4
    video_writer = None
    if SAVE_TO_FILE:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter('NadiaCoria_Demo_Mejorada.mp4', fourcc, FPS, (W, H))
        print("-> Exportando demo en 'NadiaCoria_Demo_Mejorada.mp4'...")

    print("Corriendo Demo Procedural. Presiona 'ESC' en la ventana para abortar.")
    t0 = time.perf_counter()
    
    for i in range(total_frames):
        t = i / FPS
        frame = timeline(t, rng, bufA, bufB, fire_state)
        
        # Aplicación simplificada y rápida de tus post-procesados estéticos CRT
        # Líneas de exploración de fósforo horizontales marcadas
        frame[::3, :, :] = (frame[::3, :, :].astype(np.float32) * 0.70).astype(np.uint8)
        
        # Guardar fotograma en disco
        if video_writer is not None:
            video_writer.write(frame)
            
        # Mostrar en pantalla en tiempo real
        cv2.imshow("TecNM Graficacion - Nadia Coria Argon", frame)

        elapsed = time.perf_counter() - t0
        sleep_time = ((i + 1) / FPS) - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

        if cv2.waitKey(1) & 0xFF == 27:
            print("Proceso cancelado.")
            break
            
    if video_writer is not None:
        video_writer.release()
        print("Video gurdado")
        
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()