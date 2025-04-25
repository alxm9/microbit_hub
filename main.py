import sys
import microfs
import gui, devices


Qt_app = gui.QApplication(sys.argv)
window = gui.MainWin()
table = window.con_table


def search_handler():
    window.table_clear()
    devices.search()
    if devices.connected:
        for device_id in devices.connected:
            device = devices.connected[device_id]
            window.table_add( device ) 

# Select device shown in table
def select_device():
    device_id = table.item( table.currentRow(), 1 ).data( 0 ) 
    devices.current_device = devices.connected[device_id] 
    serial = devices.current_device.serial
    show_files( serial )


# Shows files on current_device device
def show_files(serial):
    window.bottom_listbox.clear() 
    window.bottom_listbox.addItems( microfs.ls( serial = serial ) ) # Shows files on device


# Select a file from the current_devicely selected device
def select_file():
    serial = devices.current_device.serial
    microfs.ls( serial = serial )



# Establish connections between functionalities and gui
window.search_button.pressed.connect( search_handler ) 
window.con_table.pressed.connect( select_device )


window.show()

Qt_app.exec()
