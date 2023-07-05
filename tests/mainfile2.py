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
import time
from collections import deque
from data_sensor import hall_sensor

ip_actual = "10.20.0.132"

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    
    def start_streaming(self):
        self.is_streaming = True

    def stop_streaming(self):
        self.is_streaming = False

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

    video_app.run(host=ip_actual, port=5000, debug=False)


def update_graph(n):
    x_data = list(range(n))
    _, y_data = hall_sensor()

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
    '''
    video_server_process = Process(target=run_video_server)
    #video_server_process.start()

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
                html.Iframe(src="http://"+ip_actual+":5000/video_feed", width="640", height="480")
            ], style={'text-align': 'center'})
        ]
    )

    @app.callback(Output('data-stream', 'figure'), Output('message-box', 'children'),  Input('graph-update-interval', 'n_intervals'))
    def update_data_stream(n, video_server_process=video_server_process):
        data, last_value = update_graph(n)
        
        message = f"Estado de la puerta: Abierta - Valor:{last_value}" if last_value > 70 else f"Estado de la puerta: Cerrado - Valor:{last_value}"
        message_style = {'color': 'blue', 'font-size': '50px', 'text-align': 'center', 'margin': '0'}

        return data, html.Span(message, style=message_style)
    

    app.run_server(debug=True, use_reloader=True, host = "0.0.0.0", port = 8050)

    video_server_process.terminate()
    '''
    video_server_process = Process(target=run_video_server)
    video_server_process.start()

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
            html.Div(
                id='video-container',
                children=[
                    html.Img(id='live-video', src='live-video', width="640", height="480", style={'display': 'none'})
                ],
                style={'text-align': 'center'}
            )
        ]
    )

    @app.callback(
        Output('data-stream', 'figure'),
        Output('message-text', 'children'),
        Output('live-video', 'src'),
        Output('live-video', 'style'),
        Input('graph-update-interval', 'n_intervals')
    )
    def update_data_stream(n):
        data, last_value = update_graph(n)

        message = f"Estado de la puerta: Abierta - Valor:{last_value}" if last_value > 650 else f"Estado de la puerta: Cerrado - Valor:{last_value}"
        message_style = {'color': 'blue', 'font-size': '50px', 'text-align': 'center', 'margin': '0'}
        video_style = {'display': 'block'} #if last_value > 93 else {'display': 'none'}

        video_src = f"http://{ip_actual}:5000/video_feed" if last_value > 650 else ''

        return data, message, video_src, video_style

    app.run_server(host="0.0.0.0", port=8050)

    video_server_process.terminate()
