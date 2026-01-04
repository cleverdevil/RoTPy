from machine import I2C, Pin
import math
import time
import sys

from mpu6050 import MPU6050

# QT Py RP2040 STEMMA QT uses GPIO22 (SDA) and GPIO23 (SCL)
i2c = I2C(1, sda=Pin(22), scl=Pin(23), freq=400000)
mpu = MPU6050(i2c)

def get_orientation():
    ax, ay, az = mpu.read_accel()
    pitch = math.atan2(ax, math.sqrt(ay**2 + az**2)) * 180 / math.pi
    roll = math.atan2(ay, math.sqrt(ax**2 + az**2)) * 180 / math.pi
    return pitch, roll

while True:
    pitch, roll = get_orientation()
    print(f"pitch={pitch:6.1f}  roll={roll:6.1f}")
    time.sleep_ms(500)
