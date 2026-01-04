# RoTPy

RoTPy is an easy to build orientation detection sensor, including a 3D printable case,
and a webhook notification system. RoTPy is focused exclusively on rotation in the
vertical plane, making it ideal for detecting the orientation of a VESA mounted monitor
or TV.

## Required Hardware

RoTPy is designed to run on a Adafruit QT Py RP2040 with an attached Adafruit MPU-6050
6-DoF Accel and Gyro Sensor. You can acquire the two boards and a JST cable to connect
them directly from Adafruit for less than $25 as of early 2026:

- [QT Py RP2040](https://www.adafruit.com/product/4900)
- [MPU-6050 Sensor](https://www.adafruit.com/product/3886)
- [Four-pin JST cable](https://www.adafruit.com/product/4399)

Adafruit has also published
[free STL files for a snap-fit case](https://learn.adafruit.com/qt-py-snap-fit-case/3d-printing),
which can be cheaply and quickly 3D printed.

Print your case, attach the QT Py to the MPU-6050 Sensor with the JST cable, and place
the hardware into the case. This will be your RoTPy Device.

## Installation

_Note: These instructions are specific to Linux_

Once your hardware is in hand, you will first need to flash the QT Py RP2040 with the
latest version of MicroPython. First, download the latest MicroPython firmware for the
device:

```sh
wget https://micropython.org/resources/firmware/ADAFRUIT_QTPY_RP2040-20251209-v1.27.0.uf2
```

Then, hold down the "boot" button on the QT Py and attach it to your computer with a
USB-C cable and release the button after ~1s. The QT Py should then show up as a block
device, which you can verify with `lsblk`. Most modern Linux distributions will
automatically mount the block device, but you can mount it manually if needed:

```sh
udisksctl mount -b /dev/sda1`
```

Next, you will copy the MicroPython firmware to the QT Py. In my case, the device was
automounted at `/run/media/cleverdevil/RPI-RP2`:

```sh
cp ADAFRUIT_QTPY_RP2040-20251209-v1.27.0.uf2 /run/media/clever/RPI-RP2/`
```

Once the firmware has been copied to the device, it will automatically reboot, but you
can disconnect and then reconnect it from your computer if you like.

With firmware flashed, you should now be able to connect to the MicroPython REPL to
verify that installation succeeded. Note, these commands will need to be run as root, or
you will need to add your user to the `dialout` group:

```sh
sudo usermod -aG dialout $USER`
```

Once you run this command, logout and then back in, or reboot your computer so that the
change takes effect. Now that you have the required permissions, verify the installation
by connecting to the MicroPython REPL. You'll need to know the serial device, which is
usually something like `/dev/ttyACM0`, but you can verify by running `ls /dev/ttyACM*`.
Then, connect to the REPL using `screen`:

```sh
screen /dev/ttyACM0 115200
```

The REPL should appear, and you should be able to type in some Python code to verify the
version of MicroPython:

```python
import sys
sys.version
```

To exit screen: `Ctrl-A` then `K`, then `Y` to confirm.

Now its time to install RoTPy on your RoTPy device! Create yourself a `virtualenv` and
then install the required dependencies:

```sh
python -m venv venv
. venv/bin/activate
pip install pyserial mpremote
```

Now you need to copy two files to your RoTPy Device:

- `mpu6050.py` — the driver that talks to the accelerometer hardware
- `main.py` — a special Python script is automatically run when the QT Py is booted,
  which continuously reads data from the accelerometer and sends pitch/roll data over
  the USB serial interface

Use `mpremote` to copy the files and then reboot the RoTPy Device:

```sh
mpremote cp mpu6050.py :mpu6050.py
mpremote cp main.py :main.py
mpremote reset
```

Your RoTPy Device is ready to rock!

## Usage

RoTPy itself is a simple script that reads the pitch/roll data that is sent from the
hardware via a USB serial device, normalizes it into four standard orientations, and
then sends a notification to an HTTP endpoint when orientations change.

Create a `config.json` file that specifies the HTTP endpoint and a unique identifier for
that will allow the endpoint to differentiate notifications coming from different RoTPy
Devices. This repo includes an example configuration file:

```json
{
  "endpoint": "http://localhost:8080/api/orientation",
  "sensor_id": "display-1"
}
```

Now that you've built and prepared your RoTPy Device, attached it to your computer, and
created your configuration, you can finally run RoTPy:

```sh
python rotpy.py
```

The script will now monitor the orientation of your RoTPy Device continuously and send
notifications to your configured HTTP endpoint. Congrats!

## RoTPy Origins

While developing the Horizon Family Dashboard project, which will be open-sourced in
early 2026, I built RoTPy to detect the orientation of a large touchscreen monitor that
I have mounted to a wall in my home. The RoTPy allows Horizon to load portrait-oriented
and landscape-oriented dashboards based upon the orientation of the touchscreen,
creating an intuitive and familiar experience for modern smartphone and tablet users.

## License

RoTPy uses [The MIT License](https://opensource.org/license/mit).
