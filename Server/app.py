from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)


def generate_frames():
    camera_port = 0
    camera = cv2.VideoCapture(camera_port, cv2.CAP_DSHOW)  # this makes a web cam object

    while True:
        retval, im = camera.read()
        imgencode = cv2.imencode(".jpg", im)[1]
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
