import serial.tools.list_ports
from serial import Serial
import re

def check_connections():
    devices_connected = {}
    for port in serial.tools.list_ports.comports():
        if 'micro:bit' in port.description:
            devices_connected[port.device] = [port.serial_number]
    return devices_connected

def get_serial(port, dict):
    #try:
    ser = Serial(port, 115200)
    print("SHANDLER",ser)
        #dict[port].append(ser)
    #except serial.serialutil.SerialException as e:
        #return (e,port)
