#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
#dmesg | grep "tty" to find port name
import serial,time
if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')
    with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as esp:
        time.sleep(0.1) #wait for serial to open
        if esp.isOpen():
            print("{} connected!".format(esp.port))
            try:
                while True:
                    while esp.inWaiting()==0: pass
                    if  esp.inWaiting()>0: 
                        inputstr = int(esp.readline().decode('utf-8').strip())
                        inputstr = inputstr
                        print("Analog input = " + str(inputstr))
                        #dataList=answer.split("x")
                        #print("led state : {}".format(dataList[0]))
                        esp.flushInput() #remove data after reading
            except KeyboardInterrupt:
                print("KeyboardInterrupt")