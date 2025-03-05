from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QColor, QPalette, QTextCharFormat
import subprocess
import sys
from datetime import datetime

import serial_handler as shandler
import device_checker as dcheck
import microfs
import workspace



class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(840,400)
        self.setWindowTitle("Microbit Hub")

        self.main_layout = QHBoxLayout()
        self.right_layout = QVBoxLayout()
        self.left_layout = QVBoxLayout()
        self.bottom_layout = QHBoxLayout()
        self.output_layout = QVBoxLayout()

        self.right_layout.addLayout(self.output_layout,4)
        self.right_layout.addLayout(self.bottom_layout,2)

        self.main_layout.addLayout(self.left_layout,3)
        self.main_layout.addLayout(self.right_layout,7)

        self.left_placer()
        self.right_placer()

        menu = self.menuBar()
        menu_about = menu.addMenu("Help")

        bg = QWidget()
        bg.setLayout(self.main_layout)
        self.setCentralWidget(bg)

        print("This tool may ask for your password so the USB port permissions can be changed. (/dev/ttyACM...)")
        subprocess.run(['sudo','-S','ls']) # ask for password

        self.textbox.appendPlainText(
"""Click on 'Search for micro:bits' to get started.
To select a device, click on its table entry.
To change the id of a device, double click on its id name in the table.
""")

        self.connections_dict = {}
                            
    def left_placer(self):
        layout = self.left_layout

        left_text1 = QLabel("Connected micro:bits")
        left_text1.setContentsMargins(0,3,0,3)
        left_text1.setStyleSheet("color: rgb(172,172,172); font-size: 12px;")
        left_text1.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.con_table = QTableWidget(0,2,self)
        self.con_table.verticalHeader().setDefaultSectionSize(2)
        self.con_table.verticalHeader().hide()
        self.con_table.setHorizontalHeaderLabels(["Port","Device ID"])
        self.con_table.horizontalHeader().setStretchLastSection(True)
        self.con_table.horizontalScrollBar().setDisabled(True)
        self.con_table.horizontalScrollBar().setHidden(True)
        self.con_table.setRowCount(0)
        self.con_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.con_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.con_table.pressed.connect(self.load_files)
        self.con_table.cellChanged.connect(self.renamer)

        self.search_button = QPushButton("Search for micro:bits")
        self.search_button.released.connect(self.search_handler)

        self.dl_ul_layout = QHBoxLayout()
        self.dl_ul_layout.setSpacing(0)
        self.dl_all_button = QPushButton("Create workspace\n on local device")
        self.dl_all_button.setDisabled(True)
        self.dl_all_button.pressed.connect(self.create_workspace)
        self.ul_all_button = QPushButton("Flash workspace\nto micro:bits")
        self.ul_all_button.setDisabled(True)
        self.ul_all_button.pressed.connect(self.flash_workspace)
        self.ul_all_button.setContentsMargins(0,0,0,0)
        self.dl_ul_layout.addWidget(self.dl_all_button)
        self.dl_ul_layout.addWidget(self.ul_all_button)

        left_text2 = QLabel("Showing files on:")
        left_text2.setContentsMargins(0,10,0,0)
        left_text2.setStyleSheet("color: rgb(172,172,172); font-size: 12px;")
        left_text2.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.left_text3 = QLabel("None")
        self.left_text3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(left_text1,1)
        layout.addWidget(self.con_table,20)
        layout.addWidget(self.search_button)
        layout.addLayout(self.dl_ul_layout)
        layout.addWidget(left_text2,1)
        layout.addWidget(self.left_text3,10)
        layout.setSpacing(0) 

    def right_placer(self): #log, files
        self.textbox = QPlainTextEdit()
        self.textcursor = self.textbox.textCursor()
        self.textbox.setStyleSheet("background-color: rgb(0,0,0); color: rgb(255,255,255)")
        self.textbox.setReadOnly(True)
        self.textbox.setPlaceholderText("Log")
        self.output_layout.addWidget(self.textbox)

        self.red = QTextCharFormat()
        self.green = QTextCharFormat()
        self.white = QTextCharFormat()
        self.red.setForeground(QColor('red'))
        self.green.setForeground(QColor(0,255,0))
        self.white.setForeground(QColor('white'))

        self.download_button = QPushButton('Download\nto local device')
        self.download_button.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.download_button.pressed.connect(self.file_downloader)

        self.flash_button = QPushButton('Flash to\nmicro:bit ...')
        self.flash_button.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.flash_button.pressed.connect(self.file_flasher)

        self.delete_button = QPushButton('Delete\nselection')
        self.delete_button.setStyleSheet("background-color: rgb(50,0,0); color: rgb(100,100,100)")
        self.delete_button.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.delete_button.pressed.connect(self.remove_file)

        self.disable_right_buttons(disable_flash=True)

        bottom_buttons = QVBoxLayout() # relative to the right side
        bottom_buttons.setSpacing(0)
        bottom_buttons.addWidget(self.download_button)
        bottom_buttons.addWidget(self.flash_button)
        bottom_buttons.addWidget(self.delete_button)
        bottom_buttons.setContentsMargins(0,0,0,0)

        self.bottom_listbox = QListWidget()
        self.bottom_listbox.setStyleSheet("background-color: rgb(255,255,255); color: rgb(0,0,0)")
        self.bottom_listbox.pressed.connect(self.select_file)
        self.bottom_listbox.setDisabled(True)
        self.bottom_listbox.resizeEvent = self.botlb_resize
        self.right_text1 = QLabel("Download, flash, or delete\nany file after selecting a micro:bit.", self.bottom_listbox)
        self.right_text1.setStyleSheet('background: rgba(0,0,0,0); font-style: italic; padding:5px')
        self.right_text1.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignBottom)
        self.right_text1.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.bottom_layout.addWidget(self.bottom_listbox,5)
        self.bottom_layout.addLayout(bottom_buttons,1)

    def botlb_resize(self,event):
        self.right_text1.setFixedWidth(self.bottom_listbox.width())
        self.right_text1.setFixedHeight(self.bottom_listbox.height())

    def select_file(self):
        if self.download_button.isEnabled() == False:
            self.download_button.setEnabled(True)
            self.delete_button.setEnabled(True)
            self.delete_button.setStyleSheet("background-color: rgb(177,0,0); color: rgb(0,0,0)")
        self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} Selected file {self.bottom_listbox.currentIndex().data()} on device {self.grab_data('id')}")
    
    def clear_table(self):
        self.con_table.setRowCount(0)
        self.con_table.clearContents()
        del self.connections_dict
        self.connections_dict = {}

    def search_handler(self):
        self.bottom_listbox.setDisabled(True)
        self.disable_left_buttons()
        self.bottom_listbox.clear()
        self.disable_right_buttons(disable_flash=True)
        self.clear_table()

        self.connections_dict = shandler.check_connections()
        self.connections_dict = dcheck.check_devices(self.connections_dict)

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
                self.con_table.setRowCount(self.con_table.rowCount()+1)
                self.con_table.blockSignals(True) # Prevents rename device from being called upon changing the cell
                celldata = QTableWidgetItem(port)
                celldata.setFlags(celldata.flags() & ~Qt.ItemFlag.ItemIsEditable)
                print(celldata.flags())
                self.con_table.setItem(self.con_table.rowCount()-1,0,celldata)
                self.con_table.setItem(self.con_table.rowCount()-1,1,QTableWidgetItem(infolist[1]))
                self.con_table.blockSignals(False)
                self.con_table.sortItems(0)

        if (self.dl_all_button.isEnabled() == False) and (len(self.connections_dict) != 0):
            self.dl_all_button.setEnabled(True)
            self.ul_all_button.setEnabled(True)
            self.ul_all_button.setStyleSheet("background-color: rgb(255,255,0); color: rgb(0,0,0)")      

    def get_current_selections(self):
        port = self.connections_dict[self.con_table.item(self.con_table.currentRow(),0).data(0)][2]
        file = self.bottom_listbox.currentIndex().data()
        return (port, file)
    
    def file_downloader(self):
        device, file = self.get_current_selections()
        target = str(QFileDialog.getExistingDirectory(self, "Select directory"))
        if target == "":
            self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} Download operation cancelled.")
            return
        target = f'{target}/{file}'
        microfs.get(file,target=target,serial=device)
        self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} Downloaded file at {target}")

    def file_flasher(self):
        device, file = self.get_current_selections()
        target = QFileDialog.getOpenFileName()
        if target[0] == "":      
            self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} flash operation cancelled.")
            return
        file = target[0]
        microfs.put(file, serial=device)       
        self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} {file.split("/")[-1]} flashed to {self.con_table.item(self.con_table.currentRow(),0).data(0)}") 
        self.load_files(mode='refresh')

    def remove_file(self):
        device, file = self.get_current_selections()
        microfs.rm(file, device)
        self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} {file.split("/")[-1]} removed from {self.con_table.item(self.con_table.currentRow(),0).data(0)}") 
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

    def disable_right_buttons(self, disable_flash=False):
        if disable_flash:
            self.flash_button.setDisabled(True)
        self.delete_button.setDisabled(True)
        self.download_button.setDisabled(True)
        self.delete_button.setStyleSheet("")

    def load_files(self, mode = None):
        self.right_text1.setStyleSheet('background: rgba(0,0,0,0); font-style: italic; padding:5px; color: rgb(150,150,150)')
        self.bottom_listbox.setEnabled(True)
        self.disable_right_buttons()
        self.flash_button.setEnabled(True)
        port = self.con_table.item(self.con_table.currentRow(),0).data(0) #table
        self.change_current_microbit(str(port))

        if len(self.connections_dict[port]) <= 2:
            return 
        serial = self.connections_dict[port][2]
        self.bottom_listbox.clear()

        try:
            files = microfs.ls(serial=serial)
        except:
            self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} Device {port} no longer connected. Re-checking devices..")
            self.search_handler()
            return

        if not isinstance(files,list):
            self.textbox.appendPlainText(f"Permission denied. {files}")
            return
        
        self.bottom_listbox.addItems(files)

        if mode == 'refresh':
            return
        
        self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} Selected device {self.grab_data('id')} via {port}")

    def grab_data(self,colheader):
        colheader = {'serial':0,'id':1}[colheader]
        cell = self.con_table.item(self.con_table.currentRow(),colheader).data(0)
        match colheader:
            case 0: #serial
                return self.connections_dict[cell][0]
            case 1: #id
                return cell

    def create_workspace(self):
        self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} Creating workspace...")
        newdir = str(QFileDialog.getExistingDirectory(self,"Select a directory for the new workspace"))
        if newdir == '':
            self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} Create workspace operation cancelled.")
            return
        workspace_dir = workspace.create(self.connections_dict, newdir)
        
        for port, datalist in self.connections_dict.items():
            serial = datalist[2]
            for file in microfs.ls(serial=serial):
                if file == 'micro:bit-python:':
                    continue
                microfs.get(file,serial=serial,target=f"{newdir}/{workspace_dir}/{datalist[1]}/{file}")

        self.textcursor.movePosition(self.textcursor.MoveOperation.End)
        self.textcursor.insertText(f"\n{datetime.now().strftime("[%H:%M:%S]")} Created directory '/{workspace_dir}'. When flashing, please ensure all ids and directory names match and vice versa, otherwise the operation will be aborted.", self.green)
        self.textcursor.insertText(' ', self.white)

    def flash_workspace(self):
        self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} Flashing workspace...")
        flashdir = str(QFileDialog.getExistingDirectory(self,"Select a directory to flash to micro:bits"))
        if flashdir == '':
            self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} Flash workspace operation cancelled.")
            return
        
        returnee = workspace.flash_all(self.connections_dict,flashdir)
        match returnee[0]:
            case 'success':
                print("WE HERE")
                self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} Successfully flashed on all microbits.")
            case 'missing_dir':
                self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} Error: Micro:bit id '{returnee[1]}' does not match any of the directories in the given workspace. Aborting.")
            case 'missing_id':
                self.textbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} Error: Directory name '{returnee[1]}' does not match any of the connected micro:bit ids. Aborting.")
   
    def renamer(self):
        sn = self.grab_data('serial')
        id = self.grab_data('id')
        dcheck.rename_device(sn, id)
        for port, datalist in self.connections_dict.items():
            if sn in datalist:
                datalist[1] = id

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
