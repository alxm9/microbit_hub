from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction, QColor, QPalette
from PyQt6.QtCore import Qt

import sys

class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(700,400)
        self.setWindowTitle("microfs_gui")

        main_layout = QHBoxLayout()
        right_layout = QVBoxLayout()
        left_layout = QVBoxLayout()
        bottom_layout = QHBoxLayout()
        output_layout = QVBoxLayout()

        textbox = QPlainTextEdit()
        textbox.setStyleSheet("background-color: rgb(0,0,0)")
        textbox.setReadOnly(True)
        textbox.setPlaceholderText("Log")
        output_layout.addWidget(textbox)

        left_text1 = QLabel("Connected \nmicro:bits")
        left_text1.setStyleSheet("color: rgb(172,172,172); font-size: 12px;")
        left_text1.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        left_listbox1 = QListWidget()
        left_listbox1.addItems(['AA','BB'])
        left_listbox1.setStyleSheet("background-color: rgb(255,255,255); color: rgb(0,0,0)")

        chmod_button = QPushButton("chmod ttyACM0")

        left_text2 = QLabel("Currently selected")
        left_text2.setStyleSheet("color: rgb(172,172,172); font-size: 12px;")
        left_text2.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        left_text3 = QLabel("None")
        left_text3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        left_listbox2 = QListWidget()
        left_listbox2.addItems(['main.py'])
        left_listbox2.setStyleSheet("background-color: rgb(255,255,255); color: rgb(0,0,0)")

        bottom_listbox = QListWidget()
        bottom_listbox.addItems(['main.py'])
        bottom_listbox.setStyleSheet("background-color: rgb(255,255,255); color: rgb(0,0,0)")
        
        bottom_layout.addWidget(bottom_listbox)
        # bottom_layout.addWidget(button_buttons)

        left_layout.addWidget(left_text1,1)
        left_layout.addWidget(left_listbox1,20)
        left_layout.addWidget(chmod_button)
        left_layout.addWidget(left_text2,1)
        left_layout.addWidget(left_text3,10)
        # left_layout.addWidget(left_listbox2,50)

        right_layout.addLayout(output_layout,4)
        right_layout.addLayout(bottom_layout,2)

        main_layout.addLayout(left_layout,1)
        main_layout.addLayout(right_layout,5)

        bg = QWidget()
        bg.setLayout(main_layout)
        self.setCentralWidget(bg)

    def contextMenuEvent(self,e):
        context = QMenu()
        copy = QAction("copy",self)
        copy.triggered.connect(self.printer)
        context.addAction(copy)
        context.exec(e.globalPos())

    def printer(self):
        print('hello')

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