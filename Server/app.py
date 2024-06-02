from flask import Flask, render_template, Response
from flask_socketio import SocketIO
from modules.FaceRecognition import FaceRecognition
from modules.ImageRepository import ImageRepository
from flask import request
from multiprocessing.pool import ThreadPool
import cv2

app = Flask(__name__)
app.config["SECRET_KEY"] = "vnkdjnfjknfl1232#"
socketio = SocketIO(app)

connection_string = "mongodb://localhost:27017/"  # configuracao do mongo
db_name = "esp_vision"
collection_name = "imagens"
facereco = FaceRecognition(socketio)

repository = ImageRepository(connection_string, db_name, collection_name)

camera_port = 0
general_frame = None


def generate_frames():
    # this makes a web cam object
    # camera = cv2.VideoCapture("http://192.168.3.52:81/stream")
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        retval, frame = camera.read()
        if not retval:
            break
        global general_frame
        general_frame = frame
        facereco.compararFaces(frame)
        imgencode = cv2.imencode(".jpg", frame)[1]
        stringData = imgencode.tobytes()
        yield (
            b"--frame\r\n" b"Content-Type: text/plain\r\n\r\n" + stringData + b"\r\n"
        )
    camera.release()


pool = ThreadPool(processes=1)
async_result = pool.apply_async(generate_frames)


def save_face(name: str):
    imgencode = cv2.imencode(".jpg", general_frame)[1].tobytes()
    repository.salvar_imagem(imgencode, name)
    facereco.log(f"Rosto Salvo!: {name}", "rosto_salvo")
    facereco.carregarImagens()


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/save", methods=["GET", "POST"])
def save():
    data = request.get_json()
    return Response(save_face(data))


@app.route("/video")
def video():
    return Response(
        async_result.get(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    socketio.run(app, host="localhost", port=8000, debug=True)
