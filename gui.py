from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QColor, QPalette, QTextCharFormat
import sys
from datetime import datetime


"""
GUI layout:

               (main_layout)

  (left_layout)                  (right_layout)
╔══════════════╗ ╔═════════════════════════════════════════════╗
║              ║ ║                                             ║
▼              ▼ ▼                                             ▼
|
╔═══════════════╦═══════════════════════════════════════════════╗
║ left_text1    ║                                               ║
║---------------║                                               ║
║ table         ║           (output_layout)                     ║
║               ║                                               ║
║               ║               logbox                          ║
║               ║                                               ║
║---------------║                                               ║
║ search_button ║                                               ║
║ dl_ul_layout  ║-----------------------------------------------║
║ left_text2    ║           (bottom_layout)      download_button║
║ device_label  ║                                flash_button   ║
║               ║            botlist             delete_button  ║
║               ║                                               ║
╚═══════════════╩═══════════════════════════════════════════════╝


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
        self.toggle_button( "download", False )
        self.toggle_button( "flash", False )
        self.init_pressed_signals()


    def left_placer(self):

        left_text1 = QLabel("Connected micro:bits")
        left_text1.setContentsMargins(0,3,0,3)
        left_text1.setStyleSheet("color: rgb(172,172,172); font-size: 12px;")
        left_text1.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.table = QTableWidget( 0, 2, self )
        table = self.table
        table.verticalHeader().setDefaultSectionSize(2)
        table.verticalHeader().hide()
        table.setHorizontalHeaderLabels( ["Port","Device ID"] )
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalScrollBar().setDisabled(True)
        table.horizontalScrollBar().setHidden(True)
        table.setRowCount(0)
        table.setSelectionBehavior( QTableView.SelectionBehavior.SelectRows )
        table.setSelectionMode( QTableView.SelectionMode.SingleSelection )
        #table.pressed.connect(self.load_files)
        #table.cellChanged.connect(self.renamer)

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

        self.device_label = QLabel("None")
        self.device_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add everything to layout
        layout = self.left_layout
        layout.addWidget(left_text1,1)
        layout.addWidget(self.table,20)
        layout.addWidget(self.search_button)
        layout.addLayout(self.dl_ul_layout)
        layout.addWidget(left_text2,1)
        layout.addWidget(self.device_label,10)
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
        self.red.setForeground( QColor('red') )
        self.green.setForeground( QColor(0,255,0) )
        self.white.setForeground( QColor('white') )

        self.download_button = QPushButton('Download\nto local device')
        self.download_button.setSizePolicy(
                QSizePolicy.Policy.MinimumExpanding, 
                QSizePolicy.Policy.MinimumExpanding ) # horizontal, vertical
        #self.download_button.pressed.connect(self.file_downloader)

        self.flash_button = QPushButton('Flash to\nmicro:bit ...')
        self.flash_button.setSizePolicy(
                QSizePolicy.Policy.MinimumExpanding, 
                QSizePolicy.Policy.MinimumExpanding )
        #self.flash_button.pressed.connect(self.file_flasher)

        self.delete_button = QPushButton('Delete\nselection')
        self.delete_button.setStyleSheet("background-color: rgb(50,0,0); color: rgb(100,100,100)")
        self.delete_button.setSizePolicy(
                QSizePolicy.Policy.MinimumExpanding, 
                QSizePolicy.Policy.MinimumExpanding )
        #self.delete_button.pressed.connect(self.remove_file)

        #self.disable_right_buttons(disable_flash=True)

        bottom_buttons = QVBoxLayout() # relative to the right side
        bottom_buttons.setSpacing(0)
        bottom_buttons.addWidget(self.download_button)
        bottom_buttons.addWidget(self.flash_button)
        bottom_buttons.addWidget(self.delete_button)
        bottom_buttons.setContentsMargins(0,0,0,0)

        self.botlist = QListWidget()
        self.botlist.setStyleSheet("background-color: rgb(255,255,255); color: rgb(0,0,0)")
        #elf.botlist.pressed.connect(self.select_file)
        self.botlist.resizeEvent = self.botlb_resize
        self.right_text1 = QLabel("Download, flash, or delete\nany file after selecting a micro:bit.", self.botlist)
        self.right_text1.setStyleSheet('background: rgba(0,0,0,0); font-style: italic; padding:5px')
        self.right_text1.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignBottom)
        self.right_text1.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.bottom_layout.addWidget(self.botlist,5)
        self.bottom_layout.addLayout(bottom_buttons,1)


    def botlb_resize(self,event):
        self.right_text1.setFixedWidth(self.botlist.width())
        self.right_text1.setFixedHeight(self.botlist.height())


    def table_add(self, device):
        table = self.table
        port, id = QTableWidgetItem( device.port ), QTableWidgetItem( device.id )
        port.setFlags( port.flags() & ~Qt.ItemFlag.ItemIsEditable )

        table.setRowCount( table.rowCount()+1 )
        table.setItem( table.rowCount()-1, 0, port )
        table.setItem( table.rowCount()-1, 1, id )


    def table_clear(self):
        self.table.setRowCount(0)
        self.table.clearContents()


    def default_state(self):
        for button in ["flash","download","delete"]:
            self.toggle_button(button, False)
        self.change_device_label("None")


    def change_device_label(self, device_id):
        self.device_label.setText(device_id)


    def init_pressed_signals(self):

        self.table.pressed.connect( lambda: (
            self.toggle_button("flash", True),
            self.botlist.clear(),
            ))

        self.botlist.pressed.connect( lambda: (
            self.toggle_button("download", True),
            self.toggle_button("delete", True)
            ))

        self.search_button.pressed.connect( lambda: (
            self.table_clear(),
            self.default_state(),
            self.botlist.clear()
            )) 


    def toggle_button(self, in_button, state):
        button = {
                    "download": self.download_button,
                    "flash": self.flash_button,
                    "delete": self.delete_button
                }
        try:
            button[in_button].setEnabled( state )
        except KeyError:
            raise ValueError(f"Unknown button: {in_button}")


    def select_path(self):
        return QFileDialog.getOpenFileName()


    def write_log(self, to_write):
        self.logbox.appendPlainText(f"{datetime.now().strftime("[%H:%M:%S]")} {to_write}")
    

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
