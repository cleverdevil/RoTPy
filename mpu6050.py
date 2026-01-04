from machine import I2C
import struct

class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        # Wake up the MPU6050 (it starts in sleep mode)
        self.i2c.writeto_mem(self.addr, 0x6B, b'\x00')
    
    def read_accel(self):
        # Read 6 bytes starting from ACCEL_XOUT_H (0x3B)
        data = self.i2c.readfrom_mem(self.addr, 0x3B, 6)
        ax, ay, az = struct.unpack('>hhh', data)
        # Convert to g (default range is ±2g, 16384 LSB/g)
        return ax / 16384.0, ay / 16384.0, az / 16384.0
