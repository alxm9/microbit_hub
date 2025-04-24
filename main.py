import sys
import microfs
import gui, devices


Qt_app = gui.QApplication(sys.argv)
window = gui.MainWin()

def search_handler():
    window.table_clear()
    devices.search()
    if devices.connected:
        for device in devices.connected:
            window.table_add( device )


# Establish connections between functionalities and gui
window.search_button.pressed.connect( search_handler ) 


window.show()


Qt_app.exec()
