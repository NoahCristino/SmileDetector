# main.py
# import the necessary packages
from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
from WebCamera import VideoCamera
from flask_socketio import SocketIO
import logging
from sys import stdout
from camera import VideoCamera

app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(stdout))
app.config['DEBUG'] = True
socketio = SocketIO(app)
Cam = VideoCamera()

@socketio.on('input image', namespace='/test')
def test_message(input):
    input = input.split(",")[1]
    Cam.enqueue_input(input)
    #camera.enqueue_input(base64_to_pil_image(input))


@socketio.on('connect', namespace='/test')
def test_connect():
    app.logger.info("client connected")

@app.route('/')
def index():
    # rendering webpage
    return render_template('demo.html')

def gen(Camera):
    while True:
        # get camera frame
        frame = Camera.get_frame()[0]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    frame = gen(Cam)
    return Response(frame,
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video', methods=["GET", "POST"])
def video():
    r = None
    if request.method == "POST":
        req = request.form
        r = str(req['video_url'])
    if r == None:
        return redirect('index.html')
    #format received: https://www.youtube.com/watch?v=iSMbRGTBOHU
    print("url recieved: " + str(r))
    return render_template('video.html', url=r[32:])

if __name__ == '__main__':
    # defining server ip address and port
    #app.run(host='0.0.0.0', port='5000', debug=True)
    socketio.run(app)