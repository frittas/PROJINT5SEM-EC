import cv2
import face_recognition
import os
import time

class faceRecognition:
    def __init__(self):
        self.pasta_base = "Server/database"
        self.nomes_base = []
        self.imagens_base = []  

    # Carregar e codificar imagens da base
    def carregarDataBase(self):
        for nome_arquivo in os.listdir(self.pasta_base):
            # Remover a extensão do arquivo para obter o nome
            nome = os.path.splitext(nome_arquivo)[0]
            self.nomes_base.append(nome)

            caminho_arquivo = os.path.join(self.pasta_base, nome_arquivo)
            imagem_base = face_recognition.load_image_file(caminho_arquivo)
            codificacoes_base = face_recognition.face_encodings(imagem_base)

            # Verificar se pelo menos uma face foi detectada
            if codificacoes_base:
                self.imagens_base.extend(codificacoes_base)

    def compararFaces (self, frame):                
            # Encontrar faces na imagem da câmera
            face_locations = face_recognition.face_locations(frame)
            face_codificacoes = face_recognition.face_encodings(frame, face_locations)

            # Comparar cada face encontrada com a lista de imagens da base
            for face_codificacao in face_codificacoes:
                correspondencia_encontrada = False
                for codificacao_base, nome_base in zip(self.imagens_base, self.nomes_base):
                    comparacao = face_recognition.compare_faces(
                        [codificacao_base], face_codificacao)

                    if comparacao[0]:  # Se for uma correspondência
                        print(f"Rosto detectado: {nome_base}")
                        correspondencia_encontrada = True
                        break

                if not correspondencia_encontrada:
                    print("Rosto detectado, mas não está na base de dados!")