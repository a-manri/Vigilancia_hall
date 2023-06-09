import RPi.GPIO as GPIO
import time
import cv2
import paho.mqtt.client as mqtt #esto para transmitir a thingsboard
import json
import base64


#seteo de envio de datos a thingsboard
iot_hub = "demo.thingsboard.io"
port = 1883
username = "3DouW1fQOxGGWsFtddjR"
password = ""
topic = "v1/devices/me/telemetry" #revisar este, porque el nuestro está en español

client = mqtt.Client()
client.username_pw_set(username,password)
client.connect(iot_hub,port)
print("Conexión exitosa")


# Setea el modo de los pines GPIO 
GPIO.setmode(GPIO.BCM)

#pin conectado al sensor
sensor_pin = 23


#Configurar el pin del sensor como entrada
GPIO.setup(sensor_pin, GPIO.IN)

#print("Setup GPIO pin as input on GPIO16")
#GPIO.setup(sensor_pin = 16 , GPIO.IN, pull_up_down=GPIO.PUD_UP)



#función que graba el video
def grabacion_video():

    cap = cv2.VideoCapture(0)  #revisar esto bien

    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    video = cv2.VideoWriter("video_de_seguridad.mp4v", cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, size, False) #puede ser "XVID" igual, revisar esto

    

    while GPIO.input(sensor_pin):
        ret, frame = cap.read()

        if ret:
            # Esto es para hacer el livestream
            #Primero se encodea cada frame como jpg
            _, jpeg_frame = cv2.imencode(".jpg", frame)
            encoded_frame = base64.b64encode(jpeg_frame.tobytes()).decode("utf-8")

            # Se crea el mensaje a enviar con la data encodeada
            payload = {"video": encoded_frame}

            # se publica el video en thinsboard
            client.publish(topic, str(payload))

            # Se guarda el video en la raspberry pi igualmente 
            video.write(frame)

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Grabación", gray)
        cv2.waitKey(1)

    cap.release()
    video.release()
    cv2.destroyAllWindows()




data = dict()

#Código que lee el sensor, controla la grabación, manda datos del campo magnético y mensaje sobre el estado de la puerta
try:
    while True:

        time.sleep(0.1)

        sensor_value = GPIO.input(sensor_pin)

        print("Sensor value:", sensor_value)

        if sensor_value:
            # si el sensor detecta algo 
            print("Puerta abierta")
            data["GPIO-status"] = "Puerta abierta"
            data_out = json.dumps(data)
            client.publish(topic,data_out,0)
            grabacion_video()
            time.sleep(1)
        else:
            print("Puerta cerrada")
            data["GPIO-status"] = "Puerta cerrada"
            data_out = json.dumps(data)
            client.publish(topic,data_out,0)
            time.sleep(1)

        time.sleep(0.1)

#parar el código con ctrl + c
except KeyboardInterrupt:
    GPIO.cleanup()

