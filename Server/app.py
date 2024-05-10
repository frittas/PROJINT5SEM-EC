from flask import Flask, render_template, Response
import cv2

from modules.FaceRecognition import FaceRecognition
from server.modules.ImageRepository import ImageRepository

app = Flask(__name__)


connection_string = "mongodb://localhost:27017/"  # configuracao do mongo
db_name = "esp_vision"
collection_name = "imagens"
facereco = FaceRecognition()

repository = ImageRepository(connection_string, db_name, collection_name)


# camera_port = 0
# camera = cv2.VideoCapture(camera_port, cv2.CAP_DSHOW)  # this makes a web cam object

# retval, frame = camera.read()

# imgencode = cv2.imencode(".jpg", frame)[1].tostring()

# repository.salvar_imagem(imgencode, "rafael")


def generate_frames():

    camera_port = 0
    camera = cv2.VideoCapture(camera_port, cv2.CAP_DSHOW)  # this makes a web cam object

    while True:
        retval, frame = camera.read()

        reco = facereco.compararFaces(frame)
        print(f"Rosto detectado: {reco}")

        imgencode = cv2.imencode(".jpg", frame)[1]
        stringData = imgencode.tostring()
        yield (
            b"--frame\r\n" b"Content-Type: text/plain\r\n\r\n" + stringData + b"\r\n"
        )

    del camera




@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video")
def video():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True, threaded=True)
