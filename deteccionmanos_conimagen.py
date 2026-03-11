import cv2
import mediapipe as mp
import numpy as np
import math

# Configuración mediapipe
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=r'C:\Users\tigre\OneDrive\Documentos\graficacion\hand_landmarker.task'
    ),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=1
)

# cargar imagen
imagen_original = cv2.imread(r'C:\Users\tigre\Downloads\gatito doom.jpg')

# tamaño inicial
escala = 0.5

cap = cv2.VideoCapture(0)

with HandLandmarker.create_from_options(options) as landmarker:

    while cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=frame_rgb
        )

        results = landmarker.detect(mp_image)

        if results.hand_landmarks:

            hand_landmarks = results.hand_landmarks[0]

            h, w, c = frame.shape

            # coordenadas pulgar e indice
            thumb = hand_landmarks[4]
            index = hand_landmarks[8]

            x1, y1 = int(thumb.x * w), int(thumb.y * h)
            x2, y2 = int(index.x * w), int(index.y * h)

            # dibujar puntos
            cv2.circle(frame, (x1,y1),10,(255,0,0),-1)
            cv2.circle(frame, (x2,y2),10,(255,0,0),-1)

            # linea entre dedos
            cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),3)

            # distancia entre dedos
            distancia = math.hypot(x2-x1, y2-y1)

            # cambiar escala segun distancia
            escala = np.interp(distancia, [30,200], [0.5,2])

        # redimensionar imagen
        if imagen_original is not None:

            nueva = cv2.resize(
                imagen_original,
                None,
                fx=escala,
                fy=escala
            )

            ih, iw, _ = nueva.shape

            # posicion donde se mostrara
            frame[50:50+ih, 50:50+iw] = nueva

        cv2.imshow("Control de imagen con mano", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()