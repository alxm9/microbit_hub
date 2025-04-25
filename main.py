import sys
import microfs
import gui, devices


Qt_app = gui.QApplication(sys.argv)
window = gui.MainWin()

# Buttons
search = window.search_button

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

# Shows files on current_device device
def show_files():
    serial = devices.current_device.serial
    window.botlist.addItems( microfs.ls( serial = serial ) ) # Shows files on device


# Select a file from the current selected device
def select_file():
    pass
    #window.toggle_button( "download", True )




# Establish connections between functionalities and gui
search.pressed.connect( search_handler ) 
window.table.pressed.connect( select_device )
window.botlist.pressed.connect( select_file )


window.show()

Qt_app.exec()
