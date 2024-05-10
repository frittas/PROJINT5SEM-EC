import face_recognition
import os
import cv2
from server.modules.ImageRepository import ImageRepository

connection_string = "mongodb://localhost:27017/"  # configuracao do mongo
db_name = "esp_vision"
collection_name = "imagens"


class FaceRecognition:
    def __init__(self):
        self.pasta_base = "Server/database"
        self.nomes_base = []
        self.imagens_base = []
        self.repository = ImageRepository(connection_string, db_name, collection_name)
        # self.carregarImagens()
        self.carregarDataBase()

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

    def carregarImagens(self):
        documents = self.repository.bucar_todas_imagens()

    def compararFaces(self, frame) -> str:
        # Encontrar faces na imagem da câmera
        face_locations = face_recognition.face_locations(frame)
        face_codificacoes = face_recognition.face_encodings(frame, face_locations)

        # Comparar cada face encontrada com a lista de imagens da base
        for face_codificacao in face_codificacoes:
            correspondencia_encontrada = False
            for codificacao_base, nome_base in zip(self.imagens_base, self.nomes_base):
                comparacao = face_recognition.compare_faces(
                    [codificacao_base], face_codificacao
                )

                for top, right, bottom, left in face_locations:
                    image = cv2.rectangle(
                        frame, (left, top), (right, bottom), (0, 255, 0), 2
                    )

                if comparacao[0]:  # Se for uma correspondência
                    cv2.putText(
                        image,
                        nome_base,
                        (top, int(left/2)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (36, 255, 12),
                        2,
                    )
                    correspondencia_encontrada = True
                    return nome_base

            if not correspondencia_encontrada:
                cv2.putText(
                    image,
                    "INTRUSO SAI DAQUI",
                    (top, int(left/2)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 0, 255),
                    2,
                )

    def gravarFace(frame):
        return True
