import socket
import struct as s

# Raspberry PI - IP and port
rcv_UDP_IP = "0.0.0.0"
rcv_UDP_PORT = 51001

# Websocket setup
in_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
in_sock.bind((rcv_UDP_IP, rcv_UDP_PORT))

def getPosRot():
        data, addr = in_sock.recvfrom(4096) # buffer size is 1024 bytes

        pos = []
        for i in range(3): pos.append( s.unpack_from('d', data, 32+i*8)[0])

        rot = []
        for i in range(3): rot.append( s.unpack_from('d', data, 56+i*8)[0])

        return pos,rot

while True:
        print(getPosRot() )
