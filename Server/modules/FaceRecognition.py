import face_recognition
import os
import numpy as np
import cv2 as cv
from flask_socketio import SocketIO
from modules.ImageRepository import ImageRepository

connection_string = "mongodb://localhost:27017/"  # configuracao do mongo
db_name = "esp_vision"
collection_name = "imagens"
socket: SocketIO

class FaceRecognition:
    def __init__(self, socketio: SocketIO):
        self.socket = socketio
        self.pasta_base = "server/database"
        self.nomes_base = []
        self.imagens_base = []
        self.repository = ImageRepository(
            connection_string, db_name, collection_name)
        self.carregarImagens()
        # self.carregarDataBase()

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
                self.nomes_base.append(nome)

    def carregarImagens(self):
        documents = self.repository.bucar_todas_imagens()
        for doc in documents:
            image = cv.imdecode(
                np.frombuffer(doc["imagem"], dtype=np.uint8), cv.IMREAD_COLOR
            )
            face_encoding = face_recognition.face_encodings(image)
            self.imagens_base.extend(face_encoding)
            self.nomes_base.append(doc["nome"])

    def compararFaces(self, frame) -> str:
        # Encontrar faces na imagem da câmera
        frame_encoding = face_recognition.face_encodings(frame)
        face_locations = face_recognition.face_locations(frame)
        # Comparar cada face encontrada com a lista de imagens da base
        if frame_encoding:

            # Comparar cada face encontrada com a lista de imagens da base
            for face_codificacao in frame_encoding:
                correspondencia_encontrada = False
                for codificacao_base, nome_base in zip(self.imagens_base, self.nomes_base):
                    comparacao = face_recognition.compare_faces(
                        [codificacao_base], face_codificacao)

                    if comparacao[0]:  # Se for uma correspondência

                        for top, right, bottom, left in face_locations:
                            detected_image = cv.rectangle(
                                frame, (left, top), (right,
                                                     bottom), (36, 255, 12), 2
                            )
                        cv.putText(
                            detected_image,
                            nome_base,
                            (left, top - 20),
                            cv.FONT_HERSHEY_SIMPLEX,
                            0.9,
                            (36, 255, 12),
                            2,
                        )

                        print(f"Rosto detectado: {nome_base}")
                        self.socket.emit('log', f"Rosto detectado: {nome_base}")
                        correspondencia_encontrada = True
                        break

            if not correspondencia_encontrada:
                print("Rosto detectado, mas não está na base de dados!")
                self.socket.emit('log', f"Rosto não identificado!")

                for top, right, bottom, left in face_locations:
                    undetected_image = cv.rectangle(
                        frame, (left, top), (right, bottom), (0, 0, 255), 2
                    )
                cv.putText(
                    undetected_image,
                    "NAO IDENTIFICADO",
                    (left - 50, top - 20),
                    cv.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 0, 255),
                    2,
                )

                # results = face_recognition.compare_faces(
                #     self.imagens_base, frame_encoding[0]
                # )

                # for result, nome in zip(results, self.nomes_base):
                #     if result.T:
                #         for top, right, bottom, left in face_locations:
                #             image = cv.rectangle(
                #                 frame, (left, top), (right, bottom), (36, 255, 12), 2
                #             )
                #         cv.putText(
                #             image,
                #             nome,
                #             (left, top - 20),
                #             cv.FONT_HERSHEY_SIMPLEX,
                #             0.9,
                #             (36, 255, 12),
                #             2,
                #         )
                #         return nome
                #     else:
                #         for top, right, bottom, left in face_locations:
                #             image = cv.rectangle(
                #                 frame, (left, top), (right, bottom), (0, 0, 255), 2
                #             )
                #         cv.putText(
                #             image,
                #             "NAO IDENTIFICADO",
                #             (left - 50, top - 20),
                #             cv.FONT_HERSHEY_SIMPLEX,
                #             0.9,
                #             (0, 0, 255),
                #             2,
                #         )
                #         return "NAO IDENTIFICADO"

    def gravarFace(frame):
        return True
