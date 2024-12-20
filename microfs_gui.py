from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction, QColor, QPalette
from PyQt6.QtCore import Qt

import subprocess
import sys
from datetime import datetime

import serial_handler as shandler
import microfs



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

        print("This tool may ask for your password so the USB port permissions can be changed. (/dev/ttyACM...)")
        subprocess.run(['sudo','-S','ls']) # ask for password

        self.connections_dict = {}

    def left_placer(self):
        layout = self.left_layout

        left_text1 = QLabel("Micro:bit\nworkspace")
        left_text1.setStyleSheet("color: rgb(172,172,172); font-size: 12px;")
        left_text1.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.left_listbox1 = QListWidget()
        self.left_listbox1.setStyleSheet("background-color: rgb(255,255,255); color: rgb(0,0,0)")
        self.left_listbox1.pressed.connect(self.load_files)

        self.search_button = QPushButton("Search for devices")
        self.search_button.released.connect(self.search_handler)

        self.dl_all_button = QPushButton("Create workspace\non local\ndevice")
        self.dl_all_button.setDisabled(True)

        self.ul_all_button = QPushButton("Upload workspace\nto micro:bits")
        self.ul_all_button.setDisabled(True)

        left_text2 = QLabel("Showing files on:")
        left_text2.setStyleSheet("color: rgb(172,172,172); font-size: 12px;")
        left_text2.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.left_text3 = QLabel("None")
        self.left_text3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        left_listbox2 = QListWidget()
        left_listbox2.addItems(['main.py'])
        left_listbox2.setStyleSheet("background-color: rgb(255,255,255); color: rgb(0,0,0)")

        layout.addWidget(left_text1,1)
        layout.addWidget(self.left_listbox1,20)
        layout.addWidget(self.search_button)
        layout.addWidget(self.dl_all_button)
        layout.addWidget(self.ul_all_button)
        layout.addWidget(left_text2,1)
        layout.addWidget(self.left_text3,10)        

    def right_placer(self): #log, files
        self.textbox = QPlainTextEdit()
        self.textbox.setStyleSheet("background-color: rgb(0,0,0); color: rgb(255,255,255)")
        self.textbox.setReadOnly(True)
        self.textbox.setPlaceholderText("Log")
        self.output_layout.addWidget(self.textbox)

        self.download_button = QPushButton('Download\nto local device')
        self.download_button.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.download_button.pressed.connect(self.file_downloader)

        self.upload_button = QPushButton('Upload to\nmicro:bit ...')
        self.upload_button.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.upload_button.pressed.connect(self.file_uploader)

        self.delete_button = QPushButton('Delete\nselection')
        self.delete_button.setStyleSheet("background-color: rgb(50,0,0); color: rgb(100,100,100)")
        self.delete_button.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.delete_button.pressed.connect(self.remove_file)

        self.disable_right_buttons(disable_upload=True)

        bottom_buttons = QVBoxLayout() # relative to the right side
        bottom_buttons.addWidget(self.download_button)
        bottom_buttons.addWidget(self.upload_button)
        bottom_buttons.addWidget(self.delete_button)
        bottom_buttons.setContentsMargins(0,0,0,0)

        self.bottom_listbox = QListWidget()
        self.bottom_listbox.addItems(['Files will show here after selecting a device.'])
        self.bottom_listbox.setStyleSheet("background-color: rgb(255,255,255); color: rgb(0,0,0)")
        self.bottom_listbox.pressed.connect(self.select_file)
        self.bottom_listbox.setDisabled(True)

        self.bottom_layout.addWidget(self.bottom_listbox,5)
        self.bottom_layout.addLayout(bottom_buttons,1)

    def select_file(self):
        if self.download_button.isEnabled() == False:
            self.download_button.setEnabled(True)
            self.delete_button.setEnabled(True)
            self.delete_button.setStyleSheet("background-color: rgb(177,0,0); color: rgb(0,0,0)")
        self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} Selected file {self.bottom_listbox.currentIndex().data()} on device {self.left_listbox1.currentIndex().data()}")

    def clear_listbox(self):
        self.left_listbox1.clear()
        del self.connections_dict
        self.connections_dict = {}

    def search_handler(self):
        self.bottom_listbox.setDisabled(True)
        self.disable_left_buttons()
        self.bottom_listbox.clear()
        self.disable_right_buttons(disable_upload=True)
        self.clear_listbox()

        self.connections_dict = shandler.check_connections()

        if not isinstance(self.connections_dict,dict):
            QMessageBox.critical(self, 'Error', str(self.connections_dict).split(':',1)[0])
            return
        elif len(self.connections_dict) == 0:
            self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} No connections found.")
            return
        
        for port, infolist in self.connections_dict.items():
            self.change_permissions(port)
            shandler.get_serial(port,self.connections_dict)
            print(port, len(infolist), infolist)
            if len(infolist) > 1:
                self.left_listbox1.addItem(port)
                self.left_listbox1.sortItems()

        if (self.dl_all_button.isEnabled() == False) and (len(self.connections_dict) != 0):
            self.dl_all_button.setEnabled(True)
            self.ul_all_button.setEnabled(True)
            self.ul_all_button.setStyleSheet("background-color: rgb(255,255,0); color: rgb(0,0,0)")      

    def get_current_selections(self):
        return (self.connections_dict[self.left_listbox1.currentIndex().data()][1], self.bottom_listbox.currentIndex().data())
    
    def file_downloader(self):
        device, file = self.get_current_selections()
        target = str(QFileDialog.getExistingDirectory(self, "Select directory"))
        if target == "":
            self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} Download operation cancelled.")
            return
        target = f'{target}/{file}'
        microfs.get(file,target=target,serial=device)
        self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} Downloaded file at {target}")

    def file_uploader(self):
        device, file = self.get_current_selections()
        target = QFileDialog.getOpenFileName()
        print(target)
        if target[0] == "":      
            self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} Upload operation cancelled.")
            return
        file = target[0]
        microfs.put(file, serial=device)       
        self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} {file.split("/")[-1]} uploaded to {self.left_listbox1.currentIndex().data()}") 
        self.load_files(mode='refresh')

    def remove_file(self):
        device, file = self.get_current_selections()
        microfs.rm(file, device)
        self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} {file.split("/")[-1]} removed from {self.left_listbox1.currentIndex().data()}") 
        self.load_files(mode='refresh')

    def change_current_microbit(self, selection):
        self.left_text3.setText(selection)

    def change_permissions(self,port):
        subprocess.run(["sudo", "chmod", "666", port])
        self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} Device found, executed 'sudo chmod 666 {port}'")

    def disable_left_buttons(self):
        self.ul_all_button.setDisabled(True)
        self.dl_all_button.setDisabled(True)
        self.ul_all_button.setStyleSheet("")

    def disable_right_buttons(self, disable_upload=False):
        if disable_upload:
            self.upload_button.setDisabled(True)
        self.delete_button.setDisabled(True)
        self.download_button.setDisabled(True)
        self.delete_button.setStyleSheet("")

    def load_files(self, mode = None):
        self.bottom_listbox.setEnabled(True)
        self.disable_right_buttons()
        self.upload_button.setEnabled(True)
        port = self.left_listbox1.currentIndex().data()
        self.change_current_microbit(str(port))

        if len(self.connections_dict[port]) <= 1:
            return
        serial = self.connections_dict[port][1]
        self.bottom_listbox.clear()

        try:
            files = microfs.ls(serial=serial)
        except:
            self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} Device {self.left_listbox1.currentIndex().data()} no longer connected. Re-checking devices..")
            self.search_handler()
            return

        if not isinstance(files,list):
            self.textbox.appendPlainText(f"Permission denied. {files}")
            return
        
        self.bottom_listbox.addItems(files)

        if mode == 'refresh':
            return
        
        self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} Selected device at {port}")

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