import cv2
import mediapipe as mp

# Configuración de MediaPipe Tasks
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=1,
    min_hand_detection_confidence=0.7
)

def get_letter(landmarks):
    """
    Lógica simple para identificar señas basadas en la punta de los dedos 
    comparada con sus nudillos (simplificado).
    """
    # Landmarks de las puntas: 8(Índice), 12(Medio), 16(Anular), 20(Meñique)
    # Landmarks de los nudillos: 6, 10, 14, 18
    fingers = []
    
    # Dedos largos (Índice a Meñique)
    for tip, pip in zip([8, 12, 16, 20], [6, 10, 14, 18]):
        if landmarks[tip].y < landmarks[pip].y:
            fingers.append(1) # Extendido
        else:
            fingers.append(0) # Cerrado

    # Lógica de traducción simple
    if fingers == [0, 0, 0, 0]: return "A"
    if fingers == [1, 0, 0, 0]: return "1"
    if fingers == [1, 1, 0, 0]: return "V"
    if fingers == [1, 1, 1, 1]: return "B"
    if fingers == [0, 0, 0, 1]: return "I"
    
    return "?"

cap = cv2.VideoCapture(0)
mensaje = ""
ultima_letra = ""
contador_frames = 0

# ... (mismo código inicial de configuración) ...

with HandLandmarker.create_from_options(options) as landmarker:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        frame = cv2.flip(frame, 1)
        # --- SOLUCIÓN: Definir dimensiones aquí para que siempre existan ---
        h, w, _ = frame.shape 
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        results = landmarker.detect(mp_image)

        if results.hand_landmarks:
            for hand_landmarks in results.hand_landmarks:
                letra_actual = get_letter(hand_landmarks)
                
                # Ya no necesitamos definir 'h' y 'w' aquí dentro
                cv2.putText(frame, f"Letra: {letra_actual}", (50, 100), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

                # Lógica de escritura (estable por 20 frames)
                if letra_actual == ultima_letra and letra_actual != "?":
                    contador_frames += 1
                    if contador_frames > 20:
                        mensaje += letra_actual
                        ultima_letra = ""
                        contador_frames = 0
                else:
                    ultima_letra = letra_actual
                    contador_frames = 0

        # --- El dibujo del rectángulo ahora siempre tendrá el valor de 'w' ---
        cv2.rectangle(frame, (0, h - 80), (w, h), (0, 0, 0), -1)
        cv2.putText(frame, f"Texto: {mensaje}", (20, h - 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Traductor de Senas", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): break
        if key == ord('c'): mensaje = "" 

cap.release()
cv2.destroyAllWindows()

