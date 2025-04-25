import sys
import microfs
import gui, devices


Qt_app = gui.QApplication(sys.argv)
window = gui.MainWin()


def search_handler():
    devices.search()
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
def show_files():
    window.botlist.clear()
    device = devices.current_device
    window.botlist.addItems( microfs.ls( serial = device.serial ) ) # Shows files on device
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
    show_files()


# Flash a file to current device
def flash_file():
    path = window.select_path()[0]
    microfs.put( path, serial = devices.current_device.serial )
    show_files()
    window.write_log(f"Flashed '{path.split('/')[-1]}' to '{devices.current_device.id}'.")


def change_id(): 
    new_name = window.table.currentIndex().data()
    devices.current_device.rename(new_name)
    select_device()


# Establish connections between functionalities and gui
connections = [
        ( window.search_button, search_handler ),
        ( window.table, select_device ),
        ( window.botlist, select_file ),
        ( window.flash_button , flash_file ),
        ( window.delete_button , delete_file )
        ]

for gui_element, function in connections:
    gui_element.pressed.connect( function )

# More connections
window.table.cellChanged.connect( change_id )


window.show()

Qt_app.exec()
