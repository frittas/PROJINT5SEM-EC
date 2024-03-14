import cv2
import os

webcam = cv2.VideoCapture(0)

capturar_foto = False
destino = "C:/Users/Murilo/Desktop/WorkSpace/OpenCV/database"
i = 0
    
while True:
    validation, frame = webcam.read()
    if not validation:
        break

    cv2.imshow("Video", frame)   

    key = cv2.waitKey(5)     
        
    if key == 27:  # Pressione ESC para sair
        break
    elif key == 32:  # Pressione espaço para capturar uma foto
        capturar_foto = True

    if capturar_foto:
        caminho_destino = os.path.join(destino, f"foto_{i}.png")
        cv2.imwrite(caminho_destino, frame)
        print(f"Foto {i} salva em {caminho_destino}")
        capturar_foto = False
        i+=1

webcam.release()
cv2.destroyAllWindows()