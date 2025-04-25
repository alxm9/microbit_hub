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
            window.table_add( device ) 


# Seect device shown in table
def select_device():
    table = window.table
    device_id = table.item( table.currentRow(), 1 ).data( 0 ) 
    devices.current_device = devices.connected[device_id] 
    show_files()


# Shows files on current device
def show_files():
    window.botlist.clear()
    serial = devices.current_device.serial
    window.botlist.addItems( microfs.ls( serial = serial ) ) # Shows files on device


# Select a file from the current device
def select_file():
    devices.current_file = window.botlist.currentIndex().data()


# Delete current selected file
def delete_file():
    microfs.rm( devices.current_file )
    show_files()


# Flash a file to current device
def flash_file():
    path = window.select_path()[0]
    microfs.put( path, serial = devices.current_device.serial )
    show_files()


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


window.show()

Qt_app.exec()
