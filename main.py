import sys
import microfs
import gui, devices
import platform


Qt_app = gui.QApplication(sys.argv)
window = gui.MainWin()
write = window.write_log


def os_checker():
    window.write_log("Press search for micro:bits to begin.")
    window.write_log("Click on table entry to change id.\n")
    msg = {
            "Windows": "Windows detected.", # wip
            "Linux": "Linux detected. Please ensure current user is added to the 'dialout' group (sudo usermod -a -G dialout <username>), otherwise ports will frequently need to be opened manually to establish a connection. (e.g. sudo chmod 666 /dev/ttyACM0)\n",
            "Darwin": "MacOS detected." # wip
            }[platform.system()]
    window.write_log(msg)



def search_handler():

    try:
        devices.search()
    except Exception as e:
        msg = e.strerror 
        if e.errno == 13:
            msg += f". Enter 'sudo chmod 666 {msg.split()[-1]}' in terminal to open the port."
        window.write_log(f"{msg}")

    if devices.connected:
        for device_id in devices.connected:
            device = devices.connected[device_id]
            window.table.blockSignals(True) # Prevents rename device from being called upon changing the cell
            window.table_add( device ) 
            window.write_log(f"Loaded '{device.id}' on port '{device.port}'.")
            window.table.blockSignals(False)



# Select device shown in table
def select_device():
    table = window.table
    device_id = table.item( table.currentRow(), 1 ).data( 0 ) 
    devices.current_device = devices.connected[device_id] 
    window.change_device_label(device_id)
    show_files()



# Shows files on current device
def show_files(log = True):
    window.botlist.clear()
    device = devices.current_device
    window.botlist.addItems( microfs.ls( serial = device.serial ) ) # Shows files on device
    if log:
        window.write_log(f"Selected device '{device.id}'.")



# Select a file from the current device
def select_file():
    devices.current_file = window.botlist.currentIndex().data()
    window.write_log(f"Selected '{devices.current_file}' from '{devices.current_device.id}'.")



# Delete current selected file
def delete_file():
    microfs.rm( devices.current_file )
    window.write_log(f"Deleted '{devices.current_file}' from '{devices.current_device.id}'.")
    devices.current_file = None
    show_files(log = False)



# Upload file to current device
def upload_file():
    path = window.select_path()[0]
    file = path.split("/")[-1] # Used for logging

    if path == "":
        return

    try:
        microfs.put( path, serial = devices.current_device.serial )
    except Exception as e:
        window.write_log(f"{e}") #wip

    show_files(log = False)
    window.write_log(f"Uploaded '{file}' to '{devices.current_device.id}'.")



def change_id(): 
    device = devices.current_device
    new_id, old_id = window.table.currentIndex().data(), device.id
    device.rename(new_id)
    window.write_log(f"Renamed '{old_id}' to '{new_id}'.")
    select_device()



# Establish connections between functionalities and gui
connections = [
        ( window.search_button, search_handler ),
        ( window.upload_button , upload_file ),
        ( window.delete_button , delete_file )
        ]

for gui_element, function in connections:
    gui_element.released.connect( function )

# More connections
window.table.cellChanged.connect( change_id )
window.table.pressed.connect( select_device )
window.botlist.pressed.connect( select_file )


window.show()
os_checker()

Qt_app.exec()
