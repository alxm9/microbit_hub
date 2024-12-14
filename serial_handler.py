import serial.tools.list_ports
from serial import Serial
import re
import subprocess

def check_connections():
    devices_connected = []
    for port in serial.tools.list_ports.comports():
        if 'micro:bit' in port.description:
            hwid = re.search(r'[0-9A-Za-z]{4}:[0-9A-Za-z]{4}', port.hwid).group()
            devices_connected.append([port.device,hwid])
    return devices_connected

def get_serial(devices_connected):
    for device in devices_connected:       
        try:
            ser = Serial(device[0], 115200)
            device.append(ser)
        except serial.serialutil.SerialException as e:
            return (e,devices_connected)