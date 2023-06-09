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
                    #cmd=input("Enter command (data,led0 or led1): ")
                    #esp.write(cmd.encode())
                    #time.sleep(0.1) #wait for esp to answer
                    
                    while esp.inWaiting()==0: pass
                    if  esp.inWaiting()>0: 
                        answer=str(esp.readline())
                        print("---> {}".format(answer))
                        #if cmd=="data":
                        #    dataList=answer.split("x")
                        #    print("led state : {}".format(dataList[0]))
                        #    print("Analog input A0 : {}".format(dataList[1]))
                        #    print("Analog input A1: {}".format(dataList[2]))
                            
                        esp.flushInput() #remove data after reading
                            
            except KeyboardInterrupt:
                print("KeyboardInterrupt")