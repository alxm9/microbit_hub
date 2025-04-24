import sys
import gui, devices

Qt_app = gui.QApplication(sys.argv)
window = gui.MainWin()
window.show()

Qt_app.exec()
