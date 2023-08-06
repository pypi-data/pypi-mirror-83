import serial.tools.list_ports
import serial
import time
print("*初始化串口通信模块")

class MXSerial():
    def __init__(self, com, bps):
        self.ser = serial.Serial(com, bps, timeout=5)
        time.sleep(1)
    
    @classmethod
    def getCom(self,num):
        comPorts = list(serial.tools.list_ports.comports())
        ComPorts = []
        for comPort in comPorts:
            ComPorts.append(str(comPort).split(
                ' - ')[0].replace('/dev/cu.', '/dev/tty.'))
        return ComPorts[num]

    def send(self, data):
        self.ser.write(data.encode())

    def readline(self):
        return self.ser.readline().decode().strip("\r\n")

    def read(self):
        return self.ser.read().decode().strip("\r\n")

    def close(self):
        self.ser.close()


if __name__ == "__main__":

    s = MXSerial(comPorts(-1), 9600)

    while True:

        s.send(input("输入指令："))

