import serial
import sys
import os
import time
import Numeric

import struct

class E3631A:
    lf = "\r\n"

    def __init__(self, device):
        self.ser = serial.Serial(device, 9600, timeout=1, rtscts=1)

        self.send(":SYST:REM")
        self.send("*RST")
        self.send("*CLS")

        self.send("INST P25V")


    def send(self, command):
        self.ser.write(command + self.lf)

    def setVoltage(self, volt):
        self.send("VOLT %.1f"%(volt))

    def outputOn(self):
        self.send("OUTP ON")

    def outputOff(self):
        self.send("OUTP OFF")

if __name__ == "__main__":
    device = sys.argv[1]
    ea = E3631A(device)

    ea.setVoltage(15)
    ea.outputOn()

    temperatures = list(Numeric.arange(20,70,0.1))
    temperatures.reverse()
    times = 20
    Pd = 1
    Pe = 1
    Pi = 1
    epsilon = 0.3
    lastError = 0
    integral = 0

    ldusb = file("/dev/ldusb0")

    while 1:
        temperatures.reverse()
        for TD in temperatures:

            counter = 0

            while 1:
		try:
	            if ldusb.closed:
		        ldusb = file("/dev/ldusb0")
		    pkt = ldusb.read(8)
		    ldusb.close()
		    parsed_pkt = list(struct.unpack("<BBHHH", pkt))
		    T = parsed_pkt[-1] * 0.0078125
                except:
                    continue
                
                error = TD-T

                #if abs(error) < epsilon:
                #    counter += 1
                counter += 1
                if counter > times:
                    # we were long enough at the temperature, go to the next one
                    break

                dError = error - lastError

                integral += error

                v = Pd*dError + Pe*error + Pi*integral
                if v > 25:
                    v = 25
                    integral -= error
                elif v < 0:
                    v = 0
                    integral -= error
                print "TD: %.1f T: %.1f V: %.1f c: %d"%(TD, T, v, counter)
                ea.setVoltage(v)
                
                time.sleep(1)
