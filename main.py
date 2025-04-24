import sys
import microfs
import gui, devices


Qt_app = gui.QApplication(sys.argv)
window = gui.MainWin()


def search_handler():
    window.table_clear()
    devices.search()
    if devices.connected:
        for device_id in devices.connected:
            device = devices.connected[device_id]
            window.table_add( device ) 


def select_table():
    table = window.con_table
    device_id = table.item( table.currentRow(), 1 ).data( 0 ) 
    device = devices.connected[device_id] 


# Establish connections between functionalities and gui
window.search_button.pressed.connect( search_handler ) 
window.con_table.pressed.connect( select_table )


window.show()


Qt_app.exec()
