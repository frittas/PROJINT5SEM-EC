import cv2

# Inicializar a câmera
webcam = cv2.VideoCapture(0)
classificador = cv2. CascadeClassifier(r'Server/cascades/haarcascade_upperbody.xml')

while True:
    validation, frame = webcam.read()
    if not validation:
        break

    # check, frame = webcam.read()
    frameGray = cv2. cvtColor (frame,cv2.COLOR_BGR2GRAY)
    objetos = classificador.detectMultiScale(frameGray, minSize=(50,50), scaleFactor=1.5)
    # print (objetos)
    for x,y,l,a in objetos: 
        cv2. rectangle (frame,(x,y),(x+l,y+a),(255,0,0),2)
    
    cv2. imshow("Imagem", frame)
    cv2.waitKey(1)