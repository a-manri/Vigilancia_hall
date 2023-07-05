import dash
from dash import dcc
from dash import html
import random
import cv2
from flask import Flask, Response
from dash.dependencies import Input, Output
from multiprocessing import Process
import plotly.graph_objs as go
import plotly.io as pio
import threading

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

def run_video_server():
    video_app = Flask(__name__)

    def gen(camera):
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    @video_app.route('/video_feed')
    def video_feed():
        return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

    video_app.run(host='192.168.1.13', port=5000, debug=False)


def update_graph(n):
    x_data = list(range(n))
    y_data = [random.randint(0, 100) for _ in range(n)]

    data = [
        {'x': x_data, 'y': y_data, 'type': 'line', 'name': 'Data'}
    ]

    layout = {
        'title': {
            'text': 'Data del sensor en tiempo real ',
            'font': {'size': 24}
        },
        'xaxis': {
            'title': 'Time',
            'titlefont': {'size': 18},
            'tickfont': {'size': 14}
        },
        'yaxis': {
            'title': 'Data',
            'titlefont': {'size': 18},
            'tickfont': {'size': 14}
        },
        'margin': {'l': 60, 'r': 40, 't': 80, 'b': 40},
        'plot_bgcolor': '#f9f9f9',
        'paper_bgcolor': '#f9f9f9',
        'height': 400
    }

    return {'data': data, 'layout': layout}, y_data[-1]



if __name__ == '__main__':
    video_server_process = Process(target=run_video_server)
    video_server_process.start()

    #video_server_thread = threading.Thread(target=run_video_server)  # Changed to use threading.Thread
    #video_server_thread.start()  # Changed to use .start() instead of .run()

    app = dash.Dash(__name__)


    app.layout = html.Div(
        children=[
            html.Div(
                id='message-box',
                children=[
                    html.H2("Estado de la puerta: ", style={'color': 'blue', 'text-align': 'center', 'font-size': '50px'}),
                    html.P(id='message-text', style={'font-size': '50px', 'text-align': 'center', 'margin': '0'})
                ],
                style={
                    'border': '2px solid #333',
                    'border-radius': '10px',
                    'padding': '20px',
                    'background-color': '#c99ba1',
                    'width': '600px',
                    'margin': '0 auto 20px'
                }
            ),
            html.H1("Sensor en tiempo real", style={'text-align': 'center', 'font-size': '36px'}),
            dcc.Graph(id='data-stream'),
            dcc.Interval(id='graph-update-interval', interval=1000, n_intervals=0),
            html.Div([
                html.H1("Cámara de seguridad", style={'text-align': 'center', 'font-size': '36px'}),
                html.Iframe(src="http://192.168.1.13:5000/video_feed", width="640", height="480")
            ], style={'text-align': 'center'})
        ]
    )

    @app.callback(Output('data-stream', 'figure'), Output('message-box', 'children'),  Input('graph-update-interval', 'n_intervals'))
    def update_data_stream(n):
        data, last_value = update_graph(n)
        message = "Estado de la puerta: Abierta" if last_value > 40 else "Estado de la puerta: Cerrada"
        message_style = {'color': 'blue', 'font-size': '50px', 'text-align': 'center', 'margin': '0'}

        return data, html.Span(message, style=message_style)
    
    app.run_server(debug=True, use_reloader=False, host = "0.0.0.0", port = "8050")

    
    video_server_process.terminate()
