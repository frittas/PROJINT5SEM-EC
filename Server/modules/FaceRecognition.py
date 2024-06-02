import face_recognition
import os
import numpy as np
import cv2 as cv
from flask_socketio import SocketIO
from modules.ImageRepository import ImageRepository
from modules.notification import Message
import time

connection_string = "mongodb://localhost:27017/"  # configuracao do mongo
db_name = "esp_vision"
collection_name = "imagens"
socket: SocketIO
message: Message
last_sent_time: dict
send_count: dict


class FaceRecognition:
    def __init__(self, socketio: SocketIO):
        self.socket = socketio
        self.pasta_base = "server/database"
        self.nomes_base = []
        self.imagens_base = []
        self.repository = ImageRepository(connection_string, db_name, collection_name)
        self.carregarImagens()
        self.message = Message("", "")
        self.last_sent_time = {}
        self.last_sent_message = {}
        self.send_count = {}

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
                for codificacao_base, nome_base in zip(
                    self.imagens_base, self.nomes_base
                ):
                    comparacao = face_recognition.compare_faces(
                        [codificacao_base], face_codificacao
                    )

                    if comparacao[0]:  # Se for uma correspondência

                        for top, right, bottom, left in face_locations:
                            detected_image = cv.rectangle(
                                frame, (left, top), (right, bottom), (36, 255, 12), 2
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
                        self.log(f"Rosto detectado: {nome_base}", nome_base)
                        correspondencia_encontrada = True
                        break

            if not correspondencia_encontrada:
                self.log("Rosto não identificado!", "nao_identificado")

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

    def log(self, message, id):
        if self.should_send(id, 15):
            self.socket.emit("log", message)

    def should_send(self, message_id, interval):
        current_time = time.time()
        if message_id not in self.last_sent_message:
            # Se o ID da mensagem não está no dicionário, podemos enviar
            self.last_sent_message[message_id] = current_time
            self.send_count[message_id] = 1
            return True
        elif current_time - self.last_sent_message[message_id] >= interval + 1:
            # Se o intervalo de tempo for maior ou igual ao especificado, podemos enviar
            self.last_sent_message[message_id] = current_time
            self.send_count[message_id] += 1
            if (
                message_id == "nao_identificado"
                and self.send_count.get(message_id, 0) > 3
            ):
                # Se o ID é 1 e já foi tentado enviar 2 vezes, enviar agora
                self.last_sent_message[message_id] = current_time
                self.message.send(
                    "Uma pessoa não reconhecida está tentando acessar o ambiente. verificar imediatamente"
                )
                print(
                    "Uma pessoa não reconhecida está tentando acessar o ambiente. verificar imediatamente"
                )
            return True

        else:
            # Caso contrário, não enviar
            self.send_count[message_id] = self.send_count.get(message_id, 0) + 1
            return False
