import cv2
import mediapipe as mp

# 1. Configuración de MediaPipe Tasks
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# 2. DEFINICIÓN DE LA FUNCIÓN (Esto es lo que faltaba)
def get_letter(hand_landmarks):
    """
    Compara la altura (y) de las puntas de los dedos con sus nudillos 
    para determinar si el dedo está levantado (1) o bajado (0).
    """
    fingers = []
    # Puntas de los dedos: 8(Índice), 12(Medio), 16(Anular), 20(Meñique)
    # Nudillos correspondientes: 6, 10, 14, 18
    puntas = [8, 12, 16, 20]
    nudillos = [6, 10, 14, 18]

    for p, n in zip(puntas, nudillos):
        # En MediaPipe, el eje Y disminuye hacia arriba
        if hand_landmarks[p].y < hand_landmarks[n].y:
            fingers.append(1) # Dedo levantado
        else:
            fingers.append(0) # Dedo cerrado

    # Lógica de traducción simplificada
    if fingers == [0, 0, 0, 0]: return "A"
    if fingers == [1, 0, 0, 0]: return "1"
    if fingers == [1, 1, 0, 0]: return "V"
    if fingers == [1, 1, 1, 1]: return "B"
    if fingers == [0, 0, 0, 1]: return "I"
    
    return "?"

# 3. Opciones del detector
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=1,
    min_hand_detection_confidence=0.7
)

# 4. Variables de control del mensaje
mensaje = ""
ultima_letra = ""
contador_frames = 0

cap = cv2.VideoCapture(0)

with HandLandmarker.create_from_options(options) as landmarker:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        results = landmarker.detect(mp_image)

        if results.hand_landmarks:
            for hand_landmarks in results.hand_landmarks:
                letra_actual = get_letter(hand_landmarks)
                
                # Mostrar letra detectada arriba
                cv2.putText(frame, f"Detectando: {letra_actual}", (50, 60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

                # Lógica para "escribir" el mensaje
                if letra_actual == ultima_letra and letra_actual != "?":
                    contador_frames += 1
                    # Si mantienes la seña 15 frames, se agrega al texto
                    if contador_frames > 15: 
                        mensaje += letra_actual
                        ultima_letra = "" 
                        contador_frames = 0
                else:
                    ultima_letra = letra_actual
                    contador_frames = 0

        # Dibujar barra de mensaje en la parte inferior
        cv2.rectangle(frame, (0, h - 70), (w, h), (40, 40, 40), -1)
        cv2.putText(frame, f"MENSAJE: {mensaje}", (20, h - 25), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Traductor Real-Time", frame)
        
        # Teclas de control
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): break # Salir
        if key == ord('c'): mensaje = "" # Borrar mensaje

cap.release()
cv2.destroyAllWindows()