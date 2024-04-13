import cv2
import face_recognition
import os

# Carregar e codificar imagens da base
pasta_base = "Server/database"
nomes_base = []
imagens_base = []

for nome_arquivo in os.listdir(pasta_base):
    # Remover a extensão do arquivo para obter o nome
    nome = os.path.splitext(nome_arquivo)[0]
    nomes_base.append(nome)

    caminho_arquivo = os.path.join(pasta_base, nome_arquivo)
    imagem_base = face_recognition.load_image_file(caminho_arquivo)
    codificacoes_base = face_recognition.face_encodings(imagem_base)

    # Verificar se pelo menos uma face foi detectada
    if codificacoes_base:
        imagens_base.extend(codificacoes_base)

# Inicializar a câmera
webcam = cv2.VideoCapture(0)

# Inicializar o detector de corpo
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_upperbody.xml")

while True:
    validation, frame = webcam.read()
    if not validation:
        break
    
    # Encontrar corpos na imagem da câmera
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bodies = body_cascade.detectMultiScale(gray, 1.1, 4)

    # Exibir a imagem da câmera com retângulos ao redor dos corpos
    for (x, y, w, h) in bodies:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

        # Recortar a região do corpo para detectar rostos
        body_region = frame[y:y+h, x:x+w]

        # Encontrar faces na região do corpo
        face_locations = face_recognition.face_locations(body_region)
        face_codificacoes = face_recognition.face_encodings(body_region, face_locations)

        # Comparar cada face encontrada com a lista de imagens da base
        for face_codificacao in face_codificacoes:
            correspondencia_encontrada = False
            for codificacao_base, nome_base in zip(imagens_base, nomes_base):
                comparacao = face_recognition.compare_faces([codificacao_base], face_codificacao)

                if comparacao[0]:  # Se for uma correspondência
                    print(f"Rosto detectado: {nome_base}")
                    correspondencia_encontrada = True
                    break

            if not correspondencia_encontrada:
                print("Rosto detectado, mas não está na base de dados!")

    cv2.imshow("Faces", frame)

    # Pressione ESC para sair
    if cv2.waitKey(5) == 27:
        break

# Liberar recursos
webcam.release()
cv2.destroyAllWindows()
