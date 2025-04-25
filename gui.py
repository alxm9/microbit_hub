from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QColor, QPalette, QTextCharFormat
import sys


"""
GUI layout:

               (main_layout)

  (left_layout)                  (right_layout)
╔══════════════╗ ╔═════════════════════════════════════════════╗
║              ║ ║                                             ║
▼              ▼ ▼                                             ▼
|
----------------------------------------------------------------- 
| left_text1    |                                               |
|---------------|                                               |
| con_table     |           (output_layout)                     |
|               |                                               |
|               |               logbox                          |
|               |                                               |
|---------------|                                               |
| search_button |                                               |
| dl_ul_layout  |-----------------------------------------------|
| left_text2    |           (bottom_layout)      download_button|
| left_text3    |                                flash_button   |
|               |            bottom_listbox      delete_button  |
|               |                                               |
-----------------------------------------------------------------    


"""



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
        #self.con_table.pressed.connect(self.load_files)
        #self.con_table.cellChanged.connect(self.renamer)

        self.search_button = QPushButton("Search for micro:bits")
        #self.search_button.released.connect(self.search_handler)

        self.dl_ul_layout = QHBoxLayout()
        self.dl_ul_layout.setSpacing(0)
        self.dl_all_button = QPushButton("Create workspace\n on local device")
        self.dl_all_button.setDisabled(True)
        #self.dl_all_button.pressed.connect(self.create_workspace)
        self.ul_all_button = QPushButton("Flash workspace\nto micro:bits")
        self.ul_all_button.setDisabled(True)
        #self.ul_all_button.pressed.connect(self.flash_workspace)
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
        self.logbox = QPlainTextEdit()
        self.textcursor = self.logbox.textCursor()
        self.logbox.setStyleSheet("background-color: rgb(0,0,0); color: rgb(255,255,255)")
        self.logbox.setReadOnly(True)
        self.logbox.setPlaceholderText("Log")
        self.output_layout.addWidget(self.logbox)

        self.red = QTextCharFormat()
        self.green = QTextCharFormat()
        self.white = QTextCharFormat()
        self.red.setForeground(QColor('red'))
        self.green.setForeground(QColor(0,255,0))
        self.white.setForeground(QColor('white'))

        self.download_button = QPushButton('Download\nto local device')
        self.download_button.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        #self.download_button.pressed.connect(self.file_downloader)

        self.flash_button = QPushButton('Flash to\nmicro:bit ...')
        self.flash_button.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        #self.flash_button.pressed.connect(self.file_flasher)

        self.delete_button = QPushButton('Delete\nselection')
        self.delete_button.setStyleSheet("background-color: rgb(50,0,0); color: rgb(100,100,100)")
        self.delete_button.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        #self.delete_button.pressed.connect(self.remove_file)

        #self.disable_right_buttons(disable_flash=True)

        bottom_buttons = QVBoxLayout() # relative to the right side
        bottom_buttons.setSpacing(0)
        bottom_buttons.addWidget(self.download_button)
        bottom_buttons.addWidget(self.flash_button)
        bottom_buttons.addWidget(self.delete_button)
        bottom_buttons.setContentsMargins(0,0,0,0)

        self.bottom_listbox = QListWidget()
        self.bottom_listbox.setStyleSheet("background-color: rgb(255,255,255); color: rgb(0,0,0)")
        #elf.bottom_listbox.pressed.connect(self.select_file)
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

    def table_add(self, device):
        table = self.con_table
        port, id = QTableWidgetItem( device.port ), QTableWidgetItem( device.id )

        table.setRowCount( table.rowCount()+1 )
        table.setItem( table.rowCount()-1, 0, port )
        table.setItem( table.rowCount()-1, 1, id )

    def table_clear(self):
        self.con_table.setRowCount(0)
        self.con_table.clearContents()



class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)



if __name__ == "__main__":

    Qt_app = QApplication(sys.argv)

    window = MainWin()
    window.show()

    Qt_app.exec()
