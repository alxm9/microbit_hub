import os
import json
import serial.tools.list_ports
import microfs
from serial import Serial


class Microbit():

    def __init__(self, microbit_id, serial_number):
        self.id = microbit_id
        self.serial_number = serial_number

    def add_item(self):
        microfs.put()

    def remove_item(self):
        pass

    def rename(self, new_id): # not tested
        self.id = new_id
        seen_devices = grab_seen_devices()
        seen_devices[self.serial_number] = self.id
        export_seen_devices(seen_devices)
        pass




def checker_connections():

    connected_microbits = []

    for port in serial.tools.list_ports.comports():
        if "micro:bit" in port.description:
            #load json
            seen_devices = grab_seen_devices()

            print(seen_devices)
            if port.serial_number not in seen_devices:
                microbit_id = port.serial_number[16:-16]
                seen_devices[port.serial_number] = microbit_id
                export_seen_devices(seen_devices)
            else:
                microbit_id = seen_devices[port.serial_number]

            microbit = Microbit(microbit_id, port.serial_number)

            connected_microbits.append(microbit)

    print(connected_microbits)
    return connected_microbits


def export_seen_devices(seen_devices):

    json_path = grab_json_path()

    with open( json_path, "w") as output:
        json.dump(seen_devices, output, indent=6) 


def grab_seen_devices():

    json_path = grab_json_path()

    if not os.path.exists(json_path):
        with open(json_path, "w") as file:
            file.write("{}")
    
    return json.load( open("seen_devices.json") )

def grab_json_path():
    current_directory = os.getcwd()
    return os.path.join(current_directory, "seen_devices.json")


checker_connections()



# rename_device('ser1', '3')
