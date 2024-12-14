from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction, QColor, QPalette
from PyQt6.QtCore import Qt

import subprocess
import sys
from datetime import datetime

import serial_handler as shandler




class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(700,400)
        self.setWindowTitle("microfs_gui")

        self.main_layout = QHBoxLayout()
        self.right_layout = QVBoxLayout()
        self.left_layout = QVBoxLayout()
        self.bottom_layout = QHBoxLayout()
        self.output_layout = QVBoxLayout()

        self.right_layout.addLayout(self.output_layout,4)
        self.right_layout.addLayout(self.bottom_layout,2)

        self.main_layout.addLayout(self.left_layout,1)
        self.main_layout.addLayout(self.right_layout,5)

        self.left_placer()
        self.right_placer()

        menu = self.menuBar()
        menu_file = menu.addMenu("File")
        menu_preferences = menu.addMenu("Preferences")
        menu_about = menu.addMenu("About")

        bg = QWidget()
        bg.setLayout(self.main_layout)
        self.setCentralWidget(bg)

        subprocess.run(['sudo','-S','ls']) # ask for password

    def left_placer(self):
        layout = self.left_layout

        left_text1 = QLabel("Connected \nmicro:bits")
        left_text1.setStyleSheet("color: rgb(172,172,172); font-size: 12px;")
        left_text1.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # self.connections_list = shandler.check_connections()
        self.left_listbox1 = QListWidget()
        # self.left_listbox1.addItems([port[0] for port in self.connections_list])
        self.left_listbox1.setStyleSheet("background-color: rgb(255,255,255); color: rgb(0,0,0)")

        test_button = QPushButton("Search for devices")
        test_button.released.connect(self.search_handler)

        # chmod_button = QPushButton("chmod ttyACM0")
        # chmod_button.released.connect(self.change_permissions)

        left_text2 = QLabel("Current micro:bit\nselected")
        left_text2.setStyleSheet("color: rgb(172,172,172); font-size: 12px;")
        left_text2.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        left_text3 = QLabel("None")
        left_text3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        left_listbox2 = QListWidget()
        left_listbox2.addItems(['main.py'])
        left_listbox2.setStyleSheet("background-color: rgb(255,255,255); color: rgb(0,0,0)")

        layout.addWidget(left_text1,1)
        layout.addWidget(self.left_listbox1,20)
        layout.addWidget(test_button)
        # layout.addWidget(chmod_button)
        layout.addWidget(left_text2,1)
        layout.addWidget(left_text3,10)        

    def right_placer(self): #log, files
        self.textbox = QPlainTextEdit()
        self.textbox.setStyleSheet("background-color: rgb(0,0,0)")
        self.textbox.setReadOnly(True)
        self.textbox.setPlaceholderText("Log")
        self.output_layout.addWidget(self.textbox)

        download = QPushButton('Download')
        download.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        upload = QPushButton('Import')
        upload.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        remove = QPushButton('Remove')
        remove.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        bottom_buttons = QVBoxLayout() # relative to the right side
        bottom_buttons.addWidget(download)
        bottom_buttons.addWidget(upload)
        bottom_buttons.addWidget(remove)
        bottom_buttons.setContentsMargins(0,0,0,0)

        self.bottom_listbox = QListWidget()
        self.bottom_listbox.addItems(['placeholder'])
        self.bottom_listbox.setStyleSheet("background-color: rgb(255,255,255); color: rgb(0,0,0)")

        self.bottom_layout.addWidget(self.bottom_listbox,5)
        self.bottom_layout.addLayout(bottom_buttons,1)

    def search_handler(self):
        self.left_listbox1.clear()
        self.connections_list = shandler.check_connections()

        if not isinstance(self.connections_list,list):
            print(self.connections_list)
            QMessageBox.critical(self, 'Error', str(self.connections_list).split(':',1)[0])
            return
        
        for port in self.connections_list:
            self.change_permissions(port[0])
            shandler.get_serial(port)
            self.left_listbox1.addItem(port[0])
            self.left_listbox1.sortItems()


    def contextMenuEvent(self,e):
        context = QMenu()
        copy = QAction("copy",self)
        copy.triggered.connect(self.tester)
        context.addAction(copy)
        context.exec(e.globalPos())

    def change_permissions(self,port):
        self.textbox.appendPlainText(f"{datetime.now().strftime("%H:%M:%S")}: Executed sudo chmod 666 {port}")
        subprocess.run(["sudo", "chmod", "666", port])

    def show_files(self):
        self.bottom_listbox.clear()
        data = subprocess.run(["ufs", "ls"], capture_output = True)

        if 'Permission denied' in str(data.stdout):
            self.textbox.appendPlainText("Permission denied, fixing automatically")
            self.change_permissions()
            self.show_files()
            return
        
        self.textbox.appendPlainText(str(data.stdout)[2:-3])

        if 'Could not find' in str(data.stdout):
            return
        
        for index,file in enumerate(str(data.stdout)[2:-3].split()):
            self.bottom_listbox.addItems([f"{index}.{file}"])

class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

app = QApplication(sys.argv)

window = MainWin()
window.show()

app.exec()