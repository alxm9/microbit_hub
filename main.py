import sys
import microfs
import gui, devices


Qt_app = gui.QApplication(sys.argv)
window = gui.MainWin()


# Tables, lists
table = window.con_table
listbox = window.bottom_listbox

# Buttons
search = window.search_button

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
    show_files()


# Shows files on current_device device
def show_files():
    listbox.clear()
    listbox.setEnabled( True )
    serial = devices.current_device.serial
    listbox.addItems( microfs.ls( serial = serial ) ) # Shows files on device


# Select a file from the current selected device
def select_file():
    window.activate_dl()




# Establish connections between functionalities and gui
search.pressed.connect( search_handler ) 
table.pressed.connect( select_device )
listbox.pressed.connect( select_file )


window.show()

Qt_app.exec()
