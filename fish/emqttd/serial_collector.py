import serial.tools.list_ports
import serial
import time
"""
Command error, please try again. Below information may help you:
reboot					Reboot Arduino
show					Show digital pin's mode from EEPROM
init <12 pins' mode>			e.g.,init 111111111111 means set all digital pin to INPUT
allout | alloutput			Set all digital pin to OUTPUT
allin  | allinput			Set all digital pin to INPUT
setall <12 pins' mode>			e.g.,setall 000000000000 means set all digtal pin's status to HIGH
set <pin number> <pin status>		Set digital pin's status
read <pin number> <pin status>		Read pin's status or value
"""
class serial_test :
    # serialFd = -1
    #data1=''
    def __init__(self):
        print ("初始化串口类")
        plist = list(serial.tools.list_ports.comports())
        if len(plist) <= 0:
            print("没有发现端口!")
        else:
            plist_0 = list(plist[0])
            serialName = plist_0[0]
            serialFd = serial.Serial(serialName, 115200, timeout=1)
            print("可用端口名>>>", serialFd.name)
            self.serialFd = serialFd
    def set(self,command):
        self.serialFd.write(command.encode(encoding="utf-8"))
        print (command)

    def rec(self):
        while 1:
            # time.sleep(0.1)
            # print('重复')
            while self.serialFd.inWaiting():
                # time.sleep(0.5)
                self.data =self.serialFd.readlines()

                return (self.data)
    def close(self):
        self.serialFd.close()

if __name__ == '__main__':
    a = serial_test()
    print(a.rec())
    a.set(b'show')
    print(a.rec())