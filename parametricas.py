import cv2
import numpy as np
import math

def main():
    ancho, alto = 640, 480
    cx, cy = ancho // 2, alto // 2

    # --- PARÁMETROS DE LA FLOR ---
    pétalos = 5        # Si es impar, tiene 'n' pétalos. Si es par, tiene '2n'.
    radio_max = 200    # Qué tan grande es la flor
    # -----------------------------

    trayectoria = []
    longitud_max_trayectoria = 800
    frame = 0

    cv2.namedWindow("Demo Flor - Rosa de Grandi", cv2.WINDOW_AUTOSIZE)

    while True:
        img = np.zeros((alto, ancho, 3), dtype=np.uint8)

        # t es nuestro ángulo (theta) que va aumentando
        t = frame * 0.05 

        # 1. Calculamos el radio en ese ángulo específico
        # Ecuación Polar: r = a * cos(k * theta)
        r = radio_max * math.cos(pétalos * t)

        # 2. Convertimos de coordenadas polares a cartesianas (x, y)
        x = cx + r * math.cos(t)
        y = cy + r * math.sin(t)

        px, py = int(x), int(y)

        # Guardar y limitar la trayectoria
        trayectoria.append((px, py))
        if len(trayectoria) > longitud_max_trayectoria:
            trayectoria.pop(0)

        # Dibujar la estela de la flor
        for i in range(1, len(trayectoria)):
            # Color dinámico (opcional): cambia según la posición en la lista
            cv2.line(img, trayectoria[i - 1], trayectoria[i], (255, 180, 50), 2, cv2.LINE_AA)

        # Dibujar el "punto" que va trazando
        cv2.circle(img, (px, py), 5, (255, 255, 255), -1)

        cv2.imshow("Demo Flor - Rosa de Grandi", img)

        key = cv2.waitKey(16) & 0xFF
        if key == 27 or key == ord("q"):
            break

        frame += 1

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()