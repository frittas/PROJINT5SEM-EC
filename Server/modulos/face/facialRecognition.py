import cv2
import mediapipe as mp

urlCam = 'http://192.168.0.238:81/stream'
webcam = cv2.VideoCapture(0)
solucao_reconhecimento_rosto = mp.solutions.face_detection
reconhecedor_rostos = solucao_reconhecimento_rosto.FaceDetection()
desenho = mp.solutions.drawing_utils

while True:       
    validation, frame = webcam.read()
    if not validation:
        break    
    
    lista_rostos = reconhecedor_rostos.process(frame)

    if lista_rostos.detections:
        for rosto in lista_rostos.detections:
            desenho.draw_detection(frame, rosto)     
        
    cv2.imshow("Video", frame)

    key = cv2.waitKey(5)

    if key == 27:
        break

webcam.release()
cv2.destroyAllWindows()