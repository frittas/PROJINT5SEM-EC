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
# urlCam = 'http://192.168.0.238:81/stream'
webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    validation, frame = webcam.read()
    if not validation:
        break
    
    # Encontrar faces na imagem da câmera
    face_locations = face_recognition.face_locations(frame)
    face_codificacoes = face_recognition.face_encodings(frame, face_locations)

    # Comparar cada face encontrada com a lista de imagens da base
    for face_codificacao in face_codificacoes:
        correspondencia_encontrada = False
        for codificacao_base, nome_base in zip(imagens_base, nomes_base):
            comparacao = face_recognition.compare_faces(
                [codificacao_base], face_codificacao)

            if comparacao[0]:  # Se for uma correspondência
                print(f"Rosto detectado: {nome_base}")
                correspondencia_encontrada = True
                break

        if not correspondencia_encontrada:
            print("Rosto detectado, mas não está na base de dados!")

    # Exibir a imagem da câmera com retângulos ao redor das faces
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    cv2.imshow("Faces", frame)

    # Pressione ESC para sair
    if cv2.waitKey(5) == 27:
        break

# Liberar recursos
webcam.release()
cv2.destroyAllWindows()