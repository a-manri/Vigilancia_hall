import cv2
import dash
import dash_html_components as html
from dash.dependencies import Output
from flask import Flask, Response
from multiprocessing import Process

app = Flask(__name__)

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

def run_video_server():
    def gen(camera):
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    @app.route('/video_feed')
    def video_feed():
        return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

    app.run(host='192.168.1.13', port=5000, debug=False)


if __name__ == '__main__':
    video_server_process = Process(target=run_video_server)
    video_server_process.start()
    
    app = dash.Dash(__name__)
    
    app.layout = html.Div([
        html.H1("Cámara de seguridad"),
        html.Iframe(src="http://192.168.1.13:5000/video_feed", width="640", height="480")
    ])
    
    app.run_server(debug=False, use_reloader=False, host='0.0.0.0', port=8050)
    
    video_server_process.terminate()
