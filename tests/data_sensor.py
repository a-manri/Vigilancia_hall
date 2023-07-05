
import serial
import time
from collections import deque



#x_data = deque()  
y_data = deque()  

start_time = time.time()
def hall_sensor():
    with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as esp:
        time.sleep(0.1)  # Wait for serial to open
        if esp.isOpen():
            while esp.inWaiting() == 0:
                pass
            if esp.inWaiting() > 0:
                inputstr = int(esp.readline().decode('utf-8').strip())
                # Update the data collections
                #x_data.append(time.time()-start_time)
                y_data.append(inputstr)

                esp.flushInput()  # Remove data after reading
    return y_data
