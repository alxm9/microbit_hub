import serial.tools.list_ports
from serial import Serial
import re

def check_connections():
    devices_connected = {}
    for port in serial.tools.list_ports.comports():
        if 'micro:bit' in port.description:
            hwid = re.search(r'[0-9A-Za-z]{4}:[0-9A-Za-z]{4}', port.hwid).group()
            devices_connected[port.device] = [hwid]
    return devices_connected

def get_serial(port, dict):
    try:
        ser = Serial(port, 115200)
        print("port ser:",port, ser)
        dict[port].append(ser)
    except serial.serialutil.SerialException as e:
        print("HERE",e)
        return (e,port)