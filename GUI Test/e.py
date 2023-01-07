import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import qdarkstyle


app = QApplication(sys.argv)

ss_orig = app.styleSheet()
is_dark = False

def toggleStyle():
    global is_dark
    if not is_dark:
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        is_dark = True
    else:
        app.setStyleSheet(ss_orig)
        is_dark = False

toggleStyle()

w = QWidget()
w.resize(250,300)
v = QVBoxLayout(w)
#v.addWidget(QLabel("This is a test"))
cb = QComboBox()
cb.addItem(QIcon("error.png"), "Hello")  # replace with your icon file
cb.addItem(QIcon("icon.png"), "FooBar") # replace with your icon file
cb.addItem(QIcon("error.png"), "Why?!?") # replace with your icon file
v.addWidget(cb)
v.addSpacing(1)
pb = QPushButton('Toggle Dark')
pb.clicked.connect(toggleStyle)
v.addWidget(pb)
w.show()

app.exec_()