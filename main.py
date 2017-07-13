import serial
import msvcrt
import numpy as np
import time

ser = serial.Serial('COM39', 115200, timeout=100)
time.sleep(1)
ser.write("S".encode())

O2txt = open("O2.txt", "w")
minima = open("Minima.txt", "w")

history = []
window = 10
limit = 2
cntlimit = 40
cnt = cntlimit
minimum = limit

while True:

    string = ser.readline()
    O2, tau, amplitude, temperature, system_condition, battery = map(float, string.decode().split())
    O2txt.write(str(O2) + '\n')
    x = O2

    history.append(2 if x > 2 else x)
    if len(history) < window:
        continue
    history.pop(0)

    cnt -= 1
    if cnt == 0:
        minima.write(str(minimum) + '\n')
        minimum = limit
    else:
        if x < minimum and x < np.mean(history):
            minimum = x
            cnt = cntlimit

    if msvcrt.kbhit():
        if msvcrt.getwche() == '\r':
            ser.write("s".encode())
            O2txt.close()
            minima.close()
            break
