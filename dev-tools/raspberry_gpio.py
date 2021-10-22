import raspberry_socketreader as rs
from gpiozero import LED


socket = rs.viconUDP()
led = LED(17)

while 1:
    data = socket.getTimestampedData()
    if(data[3] < 60):
        led.on()
    else:
        led.off()