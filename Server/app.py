from flask import Flask, render_template, Response
import cv2

from modules.FaceRecognition import FaceRecognition
from server.modules.ImageRepository import ImageRepository



from multiprocessing.pool import ThreadPool

app = Flask(__name__)


connection_string = "mongodb://localhost:27017/"  # configuracao do mongo
db_name = "esp_vision"
collection_name = "imagens"
facereco = FaceRecognition()

repository = ImageRepository(connection_string, db_name, collection_name)

camera_port = 0
camera = cv2.VideoCapture(camera_port)  # this makes a web cam object

def generate_frames():
   
    while True:
        retval, frame = camera.read()
        if not retval:
            break

        reco = facereco.compararFaces(frame)
        if reco:
            print(f"Rosto detectado: {reco}")

        imgencode = cv2.imencode(".jpg", frame)[1]
        stringData = imgencode.tobytes()
        yield (
            b"--frame\r\n" b"Content-Type: text/plain\r\n\r\n" + stringData + b"\r\n"
        )


pool = ThreadPool(processes=1)
async_result = pool.apply_async(generate_frames)


def save_face():
    retval, frame = camera.read()
    imgencode = cv2.imencode(".jpg", frame)[1].tobytes()
    repository.salvar_imagem(imgencode, "Rafael")
    facereco.carregarImagens()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/save")
def save():
    return Response(save_face())


@app.route("/video")
def video():
    return Response(
        async_result.get(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True, threaded=True)
