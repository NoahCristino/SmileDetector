# main.py
# import the necessary packages
from flask import Flask, render_template, Response, request, redirect, url_for
from WebCamera import VideoCamera

app = Flask(__name__)

@app.route('/')
def index():
    # rendering webpage
    return render_template('index.html')

def gen(camera):
    while True:
        # get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
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
    if len(r[32:]) < 10:
        return render_template('video.html', url=r[32:])

if __name__ == '__main__':
    # defining server ip address and port
    app.run(host='0.0.0.0', port='5000', debug=True)
