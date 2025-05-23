import os
import json
import serial.tools.list_ports
from serial import Serial


connected = {}

current_device = None # current_device selected device 
current_file = None

class Microbit():

    def __init__(self, port, serial_number, microbit_id):
        self.port = port
        self.id = microbit_id # Randomly assigned id, can be changed by user
        self.sn = serial_number # Used as json key
        self.serial = Serial( self.port, 115200 ) # Serial object
        self.filelist = []
        connected[self.id] = self.serial


    def rename(self, new_id):
        del connected[self.id]
        self.id = new_id
        connected[self.id] = self
        seen_devices = grab_seen_devices()
        seen_devices[self.sn] = self.id
        export_seen_devices( seen_devices )



def search():

    connected.clear()

    for port in serial.tools.list_ports.comports():
        if "micro:bit" in port.description:

            #load json
            seen_devices = grab_seen_devices()

            device, sn = port.device, port.serial_number

            if sn not in seen_devices:
                microbit_id = sn[16:-16]
                seen_devices[sn] = microbit_id
                export_seen_devices( seen_devices )
            else:
                microbit_id = seen_devices[sn]

            connected[microbit_id] = Microbit(device, sn, microbit_id)



def export_seen_devices(seen_devices):
    json_path = grab_json()

    with open(json_path, "w") as output:
        json.dump( seen_devices, output, indent=6 ) 



def grab_seen_devices():
    json_path = grab_json()

    if not os.path.exists(json_path):
        with open(json_path, "w") as file:
            file.write("{}")
    
    return json.load( open("seen_devices.json") )



def grab_json():
    current_directory = os.getcwd()
    return os.path.join( current_directory, "seen_devices.json" )



if __name__ == "__main__":
    search()
    print(connected)

