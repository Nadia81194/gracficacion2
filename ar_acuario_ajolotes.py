from __future__ import annotations
import sys
import time
from pathlib import Path
import cv2
import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

# configuracion general
camera_index = 0
marker_length_m = 0.10  # tamano del marcador en metros
aruco_dict = cv2.aruco.DICT_4X4_50
marker_id = 0  
window_title = "ra mega acuario minecraft extremo esc salir"
znear, zfar = 0.01, 100.0

calib_npz = Path("camera_ar.npz")

# genera matriz de camara por defecto si no hay calibracion
def default_camera_matrix(width: int, height: int) -> np.ndarray:
    f = float(max(width, height))
    cx, cy = width / 2.0, height / 2.0
    return np.array([[f, 0, cx], [0, f, cy], [0, 0, 1]], dtype=np.float64)

# carga los parametros de calibracion de la camara desde el archivo npz
def load_calibration(width: int, height: int):
    if calib_npz.is_file():
        data = np.load(calib_npz)
        return data["camera_matrix"], data["dist_coeffs"]
    return default_camera_matrix(width, height), np.zeros((5, 1), dtype=np.float64)

# inicializa el detector de marcadores aruco de opencv
def make_aruco_detector():
    dictionary = cv2.aruco.getPredefinedDictionary(aruco_dict)
    params = cv2.aruco.DetectorParameters()
    if hasattr(cv2.aruco, "ArucoDetector"):
        return cv2.aruco.ArucoDetector(dictionary, params), dictionary
    return None, dictionary

# busca el marcador aruco con el id correcto en la imagen de la camara
def detect_marker(gray, detector, dictionary):
    if detector is not None:
        corners, ids, _ = detector.detectMarkers(gray)
    else:
        corners, ids, _ = cv2.aruco.detectMarkers(gray, dictionary, parameters=cv2.aruco.DetectorParameters())
    if ids is None or len(ids) == 0:
        return None
    idx = 0
    if marker_id is not None:
        matches = np.where(ids.flatten() == marker_id)[0]
        if len(matches) == 0:
            return None
        idx = int(matches[0])
    return corners[idx]

# calcula la posicion y rotacion del marcador usando solvepnp
def estimate_pose(corners, camera_matrix, dist_coeffs):
    s = marker_length_m / 2.0
    obj_pts = np.array([[-s, s, 0], [s, s, 0], [s, -s, 0], [-s, -s, 0]], dtype=np.float32)
    image_points = corners[0] if corners.ndim == 3 else corners
    image_points = np.asarray(image_points, dtype=np.float32).reshape(-1, 2)
    flags = cv2.SOLVEPNP_IPPE_SQUARE if hasattr(cv2, "SOLVEPNP_IPPE_SQUARE") else cv2.SOLVEPNP_ITERATIVE
    ok, rvec, tvec = cv2.solvePnP(obj_pts, image_points, camera_matrix, dist_coeffs, flags=flags)
    if not ok:
        raise RuntimeError("solvepnp fallo")
    return rvec, tvec

# transforma los parametros de la camara en una matriz de proyeccion opengl
def projection_from_k(K, width, height, znear, zfar):
    fx, fy = K[0, 0], K[1, 1]
    cx, cy = K[0, 2], K[1, 2]
    P = np.zeros((4, 4), dtype=np.float32)
    P[0, 0] = 2.0 * fx / width
    P[1, 1] = 2.0 * fy / height
    P[0, 2] = (width - 2.0 * cx) / width
    P[1, 2] = (2.0 * cy - height) / height
    P[2, 2] = -(zfar + znear) / (zfar - znear)
    P[2, 3] = -1.0
    P[3, 2] = -2.0 * zfar * znear / (zfar - znear)
    return P

# convierte los vectores de rotacion y traslacion en matriz modelview de opengl
def modelview_from_pose(rvec, tvec) -> np.ndarray:
    R, _ = cv2.Rodrigues(rvec)
    M = np.eye(4, dtype=np.float64)
    M[:3, :3] = R
    M[:3, 3] = tvec.flatten()
    cv_to_gl = np.diag([1.0, -1.0, -1.0, 1.0])
    return (cv_to_gl @ M).T.astype(np.float32)

# dibuja un cubo usando caras cuadradas con sus respectivas normales
def draw_cube(size_x: float, size_y: float, size_z: float):
    x, y, z = size_x / 2.0, size_y / 2.0, size_z / 2.0
    glBegin(GL_QUADS)
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(-x, -y, z); glVertex3f(x, -y, z); glVertex3f(x, y, z); glVertex3f(-x, y, z)
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(-x, -y, -z); glVertex3f(-x, y, -z); glVertex3f(x, y, -z); glVertex3f(x, -y, -z)
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(-x, y, -z); glVertex3f(-x, y, z); glVertex3f(x, y, z); glVertex3f(x, y, -z)
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(-x, -y, -z); glVertex3f(x, -y, -z); glVertex3f(x, -y, z); glVertex3f(-x, -y, z)
    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f(x, -y, -z); glVertex3f(x, y, -z); glVertex3f(x, y, z); glVertex3f(x, -y, z)
    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(-x, -y, -z); glVertex3f(-x, -y, z); glVertex3f(-x, y, z); glVertex3f(-x, y, -z)
    glEnd()

# modelado jerarquico de ajolote estilo minecraft con cola y patas articuladas
def draw_minecraft_axolotl(t: float, base_color: tuple, detail_color: tuple):
    swim_angle = np.sin(t * 12.0) * 22.0  # calculo de angulo de nado para la cola
    leg_angle = np.sin(t * 12.0) * 18.0  # calculo de angulo de braceo para las patas

    glPushMatrix()
    glScalef(0.55, 0.55, 0.55)  # escala el tamano del ajolote
    
    # cuerpo principal
    glColor3fv(base_color)
    draw_cube(3.0, 2.0, 6.0)

    # cabeza
    glPushMatrix()
    glTranslatef(0.0, 0.2, 4.0)
    glColor3fv(base_color)
    draw_cube(4.0, 2.5, 3.0)
    
    # ojos
    glColor3f(0.15, 0.08, 0.08)
    glPushMatrix(); glTranslatef(2.01, 0.2, 0.5); draw_cube(0.05, 0.5, 0.5); glPopMatrix()
    glPushMatrix(); glTranslatef(-2.01, 0.2, 0.5); draw_cube(0.05, 0.5, 0.5); glPopMatrix()

    # branquias laterales
    glColor3fv(detail_color)
    glPushMatrix(); glTranslatef(2.5, 1.0, -0.5); draw_cube(1.5, 1.5, 0.4); glPopMatrix()
    glPushMatrix(); glTranslatef(-2.5, 1.0, -0.5); draw_cube(1.5, 1.5, 0.4); glPopMatrix()
    glPopMatrix()

    # cola articulada que hereda el movimiento de seno
    glPushMatrix()
    glTranslatef(0.0, 0.0, -3.0)
    glRotatef(swim_angle, 0.0, 1.0, 0.0)
    glTranslatef(0.0, 0.0, -2.0)
    glColor3fv(base_color)
    draw_cube(1.0, 1.5, 4.0)
    
    # aleta de la cola
    glColor3fv(detail_color)
    glTranslatef(0.0, 0.0, -2.2)
    draw_cube(0.2, 2.5, 1.5)
    glPopMatrix()

    # patitas traseras y delanteras moviles
    glPushMatrix(); glTranslatef(1.6, -1.0, 2.0); glRotatef(leg_angle, 1.0, 0.0, 0.0); draw_cube(0.6, 1.0, 0.6); glPopMatrix()
    glPushMatrix(); glTranslatef(-1.6, -1.0, 2.0); glRotatef(-leg_angle, 1.0, 0.0, 0.0); draw_cube(0.6, 1.0, 0.6); glPopMatrix()
    glPushMatrix(); glTranslatef(1.6, -1.0, -2.0); glRotatef(-leg_angle, 1.0, 0.0, 0.0); draw_cube(0.6, 1.0, 0.6); glPopMatrix()
    glPushMatrix(); glTranslatef(-1.6, -1.0, -2.0); glRotatef(leg_angle, 1.0, 0.0, 0.0); draw_cube(0.6, 1.0, 0.6); glPopMatrix()

    glPopMatrix()

# modelado de pez tropical con cola oscilante rapida
def draw_tropical_fish(t: float, body_color: tuple, fin_color: tuple):
    tail_swing = np.sin(t * 20.0) * 28.0
    glPushMatrix()
    glScalef(0.25, 0.25, 0.25)
    
    # cuerpo del pez
    glColor3fv(body_color)
    draw_cube(1.0, 1.8, 2.6)
    
    # aleta superior
    glColor3fv(fin_color)
    glPushMatrix(); glTranslatef(0.0, 1.2, -0.2); draw_cube(0.18, 0.7, 1.2); glPopMatrix()
    
    # cola oscilante
    glPushMatrix()
    glTranslatef(0.0, 0.0, -1.3)
    glRotatef(tail_swing, 0.0, 1.0, 0.0)
    glTranslatef(0.0, 0.0, -0.6)
    draw_cube(0.12, 1.3, 0.8)
    glPopMatrix()
    glPopMatrix()

# genera un alga encadenando segmentos cubicos que rotan de forma acumulativa
def draw_kelp(t: float, segments: int, offset_phase: float):
    glPushMatrix()
    wave = np.sin(t * 2.2 + offset_phase) * 5.5
    for _ in range(segments):
        glRotatef(wave, 1.0, 0.0, 0.0)
        glRotatef(wave * 0.4, 0.0, 0.0, 1.0)
        glColor3f(0.12, 0.42, 0.12)
        draw_cube(1.0, 1.8, 1.0)
        glTranslatef(0.0, 1.8, 0.0)
    glPopMatrix()

# dibuja el acuario interior, suelo bloques de coral y agua transparente
def draw_aquarium(t: float):
    size = 30.0
    
    # suelo de arena
    glColor3f(0.83, 0.78, 0.62)
    glPushMatrix(); glTranslatef(0.0, -14.5, 0.0); draw_cube(29.8, 1.0, 29.8); glPopMatrix()
    
    # bloques de coral de fuego de tubo y de cerebro
    glColor3f(0.95, 0.2, 0.2)
    glPushMatrix(); glTranslatef(-3.0, -13.5, -2.0); draw_cube(2.5, 2.5, 2.5); glPopMatrix()
    glColor3f(0.1, 0.3, 0.9)
    glPushMatrix(); glTranslatef(4.0, -13.5, 3.0); draw_cube(2.0, 3.5, 2.0); glPopMatrix()
    glColor3f(0.95, 0.4, 0.7)
    glPushMatrix(); glTranslatef(-1.0, -13.5, 5.0); draw_cube(3.0, 1.5, 2.0); glPopMatrix()

    # coloca las seis columnas de algas marinas animadas en el fondo
    glPushMatrix(); glTranslatef(-11.0, -14.0, -11.0); draw_kelp(t, 9, 0.0); glPopMatrix()
    glPushMatrix(); glTranslatef(-12.0, -14.0, 6.0); draw_kelp(t, 12, 2.3); glPopMatrix()
    glPushMatrix(); glTranslatef(11.0, -14.0, -9.0); draw_kelp(t, 10, 1.1); glPopMatrix()
    glPushMatrix(); glTranslatef(10.0, -14.0, 10.0); draw_kelp(t, 7, 3.8); glPopMatrix()
    glPushMatrix(); glTranslatef(-6.0, -14.0, -12.0); draw_kelp(t, 11, 1.5); glPopMatrix()
    glPushMatrix(); glTranslatef(12.0, -14.0, -1.0); draw_kelp(t, 8, 0.7); glPopMatrix()

    # renderizado del agua usando transparencias de canal alfa alpha blend
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDepthMask(GL_FALSE)
    glColor4f(0.0, 0.5, 0.85, 0.15) 
    draw_cube(size, size, size)
    glDepthMask(GL_TRUE)

    # lineas del marco exterior de cristal
    glDisable(GL_LIGHTING)
    glLineWidth(3.0)
    glColor3f(0.7, 0.85, 0.95)
    h = size / 2.0
    glBegin(GL_LINES)
    glVertex3f(-h,-h,-h); glVertex3f(h,-h,-h);  glVertex3f(h,-h,-h); glVertex3f(h,-h,h)
    glVertex3f(h,-h,h); glVertex3f(-h,-h,h);   glVertex3f(-h,-h,h); glVertex3f(-h,-h,-h)
    glVertex3f(-h,h,-h); glVertex3f(h,h,-h);    glVertex3f(h,h,-h); glVertex3f(h,h,h)
    glVertex3f(h,h,h); glVertex3f(-h,h,h);     glVertex3f(-h,h,h); glVertex3f(-h,h,-h)
    glVertex3f(-h,-h,-h); glVertex3f(-h,h,-h);  glVertex3f(h,-h,-h); glVertex3f(h,h,-h)
    glVertex3f(h,-h,h); glVertex3f(h,h,h);      glVertex3f(-h,-h,h); glVertex3f(-h,h,h)
    glEnd()
    
    glEnable(GL_LIGHTING)
    glDisable(GL_BLEND)

# configura el sistema basico de iluminacion difusa y ambiental
def setup_lighting() -> None:
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glLightfv(GL_LIGHT0, GL_POSITION, (1.0, 2.0, 1.0, 0.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.45, 0.45, 0.45, 1.0))

_tex_id = None
_tex_buf = None

# carga la imagen en tiempo real de opencv como textura de fondo opengl
def upload_frame_texture(frame_bgr, width, height) -> None:
    global _tex_id, _tex_buf
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    rgb = cv2.flip(rgb, 0)
    if _tex_buf is None or _tex_buf.shape[:2] != (height, width):
        _tex_buf = np.empty((height, width, 3), dtype=np.uint8)
    np.copyto(_tex_buf, rgb)
    if _tex_id is None:
        _tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, _tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, _tex_buf)

# dibuja el plano bidimensional de fondo usando la textura de la camara
def draw_background_quad(width, height) -> None:
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix(); glLoadIdentity(); glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix(); glLoadIdentity()
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, _tex_id)
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(0, 0)
    glTexCoord2f(1, 0); glVertex2f(width, 0)
    glTexCoord2f(1, 1); glVertex2f(width, height)
    glTexCoord2f(0, 1); glVertex2f(0, height)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION); glPopMatrix()
    glMatrixMode(GL_MODELVIEW); glEnable(GL_DEPTH_TEST)

# funcion principal del programa control del ciclo de renderizado y captura de video
def main() -> None:
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("no se pudo abrir la camara", file=sys.stderr)
        sys.exit(1)
    ret, probe = cap.read()
    if not ret: sys.exit(1)
    cam_h, cam_w = probe.shape[:2]
    
    camera_matrix, dist_coeffs = load_calibration(cam_w, cam_h)
    detector, dictionary = make_aruco_detector()

    if not glfw.init(): sys.exit(1)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    window = glfw.create_window(cam_w, cam_h, window_title, None, None)
    if not window:
        glfw.terminate()
        sys.exit(1)
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    # callback para cerrar la aplicacion con la tecla escape o q
    def on_key(win, key, _scancode, action, _mods):
        if action == glfw.PRESS and key in (glfw.KEY_ESCAPE, glfw.KEY_Q):
            glfw.set_window_should_close(win, True)
    glfw.set_key_callback(window, on_key)

    glEnable(GL_DEPTH_TEST)

    # definicion de las variables de color para las cinco especies de ajolotes
    pink_b, pink_d = (1.0, 0.71, 0.75), (1.0, 0.4, 0.6)       
    cyan_b, cyan_d = (0.65, 0.85, 1.0), (1.0, 0.55, 0.7)      
    wild_b, wild_d = (0.45, 0.30, 0.20), (0.25, 0.15, 0.10)   
    gold_b, gold_d = (0.98, 0.85, 0.25), (0.95, 0.50, 0.0)    
    rare_b, rare_d = (0.45, 0.35, 0.90), (0.20, 0.10, 0.50)    

    # ciclo principal activo mientras la ventana este abierta
    while not glfw.window_should_close(window):
        ret, frame = cap.read()
        if not ret: continue
        h, w = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners = detect_marker(gray, detector, dictionary)

        glViewport(0, 0, w, h)
        upload_frame_texture(frame, w, h)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_background_quad(w, h)

        # codigo ejecutado unicamente si se detecta el marcador aruco id 0
        if corners is not None:
            rvec, tvec = estimate_pose(corners, camera_matrix, dist_coeffs)
            
            P = projection_from_k(camera_matrix, w, h, znear, zfar)
            MV = modelview_from_pose(rvec, tvec)
            
            glMatrixMode(GL_PROJECTION)
            glLoadMatrixf(P)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glMultMatrixf(MV)
            
            setup_lighting()
            
            # escalado global del sistema de ra sobre el marcador
            glPushMatrix()
            glScalef(0.005, 0.005, 0.005) 
            
            t = time.time()
            
            # renderiza la pecera con su fondo marino
            draw_aquarium(t)

            # renderizado iterativo del cardumen de peces en sentido horario
            for i in range(3):
                glPushMatrix()
                angle_offset = i * 120.0
                glRotatef(t * 75.0 + angle_offset, 0.0, 1.0, 0.0)
                y_pos = -3.0 + i * 2.5 + np.sin(t * 4.0 + i) * 1.5
                glTranslatef(5.5, y_pos, 0.0)
                if i == 0: draw_tropical_fish(t, (1.0, 0.5, 0.0), (1.0, 0.9, 0.0))  
                elif i == 1: draw_tropical_fish(t, (0.1, 0.8, 0.8), (1.0, 0.4, 0.4)) 
                else: draw_tropical_fish(t, (0.9, 0.9, 0.1), (0.2, 0.2, 0.8))       
                glPopMatrix()

            # renderizado iterativo del cardumen de peces en sentido antihorario
            for i in range(3):
                glPushMatrix()
                angle_offset = i * 120.0 + 60.0
                glRotatef(-t * 85.0 + angle_offset, 0.0, 1.0, 0.0)
                y_pos = 1.0 + i * 2.0 + np.cos(t * 3.5 + i) * 1.2
                glTranslatef(8.5, y_pos, 0.0)
                if i == 0: draw_tropical_fish(t, (0.4, 0.9, 0.0), (0.9, 0.0, 0.5))  
                elif i == 1: draw_tropical_fish(t, (0.9, 0.4, 0.1), (0.1, 0.9, 0.9)) 
                else: draw_tropical_fish(t, (0.7, 0.2, 0.9), (0.9, 0.9, 0.9))       
                glPopMatrix()

            # renderizado individual y posicionamiento de los cinco ajolotes grandes
            glPushMatrix()
            glRotatef(t * 30.0, 0.0, 1.0, 0.0)
            glTranslatef(8.0, -6.5, 0.0) 
            draw_minecraft_axolotl(t, pink_b, pink_d)
            glPopMatrix()

            glPushMatrix()
            glRotatef(-t * 38.0 + 72.0, 0.0, 1.0, 0.0) 
            glTranslatef(9.0, -2.0, 0.0) 
            draw_minecraft_axolotl(t + 0.4, cyan_b, cyan_d) 
            glPopMatrix()

            glPushMatrix()
            glRotatef(t * 44.0 + 144.0, 0.0, 1.0, 0.0)
            glTranslatef(7.0, 2.0 + np.cos(t * 2.5) * 2.0, 0.0) 
            draw_minecraft_axolotl(t + 0.8, wild_b, wild_d)
            glPopMatrix()

            glPushMatrix()
            glRotatef(-t * 32.0 + 216.0, 0.0, 1.0, 0.0)
            glTranslatef(10.0, 5.0 + np.sin(t * 2.0) * 1.5, 0.0) 
            draw_minecraft_axolotl(t + 1.2, gold_b, gold_d)
            glPopMatrix()

            glPushMatrix()
            glRotatef(t * 52.0 + 288.0, 0.0, 1.0, 0.0)
            glTranslatef(4.5, -1.0 + np.sin(t * 4.0) * 3.0, 0.0) 
            draw_minecraft_axolotl(t + 1.6, rare_b, rare_d)
            glPopMatrix()
            
            glPopMatrix()

        glfw.swap_buffers(window)
        glfw.poll_events()

    cap.release()
    glfw.terminate()

if __name__ == "__main__":
    main()