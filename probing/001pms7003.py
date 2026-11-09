import serial

if __name__ == "__main__":
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    while True:
        data = ser.read(32)
        print(data)
    ser.close()
