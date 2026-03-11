import cv2 as cv 

rostro = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
cap = cv.VideoCapture(0)

while True:
    ret, img = cap.read()
    if not ret:
        break

    gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gris, 1.3, 5)

    for(x,y,w,h) in rostros:

        img = cv.rectangle(img, (x,y), (x+w, y+h), (234,23,23), 3)

        # OJOS
        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.35)), 20, (255,255,255), -1)
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.35)), 20, (255,255,255), -1)
        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.35)), 6, (0,0,0), -1)
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.35)), 6, (0,0,0), -1)

        # NARIZ
        img = cv.circle(img,(x + int(w*0.5), y + int(h*0.55)),int(w*0.08),(0,0,255),-1)

        # BIGOTE
        img = cv.ellipse(img,(x + int(w*0.45), y + int(h*0.65)),(int(w*0.12), int(h*0.05)),0, 0, 180,(0,0,0),-1)
        img = cv.ellipse(img,(x + int(w*0.55), y + int(h*0.65)),(int(w*0.12), int(h*0.05)),0, 0, 180,(0,0,0),-1)

        # BOCA TRISTE
        img = cv.ellipse(img,(x + int(w*0.5), y + int(h*0.8)),(int(w*0.25), int(h*0.1)), 0, 180, 360, (0,0,0),4)

        # OREJAS
        img = cv.ellipse(img,(x - int(w*0.15), y + int(h*0.5)),(int(w*0.2), int(h*0.35)), 0, 0, 360,(150,150,150),-1)
        img = cv.ellipse(img,(x + w + int(w*0.15), y + int(h*0.5)),(int(w*0.2), int(h*0.35)),0, 0, 360,(150,150,150), -1)

        img2 = img[y:y+h, x:x+w]
        cv.imshow('img2', img2)

    cv.imshow('img', img)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()