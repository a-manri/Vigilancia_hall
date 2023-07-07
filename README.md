# Vigilancia_hall
Sistema de vigilancia para puertas con sensor hall de campo magnético

## Tres archivos fundamentales:
- video_server.py: archivo main, corre en la raspberry pi en permanencia. Recibe los datos del sensor y los publica en una dirección en la red local, además, cuando los valores del sensor superan un umbral determinado, el streaming de una cámara conectada a la raspberry comienza a ser mostrado en la dirección en la red local 

- SerialESP.ino: corre en una Wemos D1 mini pro, que actúa como interface entre el sensor linear hall KY-024 y la raspberry pi, enviando los valores de la salida analógica del sensor via conexión serial con la raspberry

- data_sensor.py: es una función auxiliar que lee los datos recividos en el puerto serial
