import smbus

RPI_ADDRESS = 0x10
bus = smbus.SMBus(0)

def writeInt(a):
    bus.write_byte(RPI_ADDRESS,a)
    a = a >> 8
    bus.write_byte(RPI_ADDRESS,a)
    
message = 4251

writeInt(message)
