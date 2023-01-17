from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt, QFile, QTextStream
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon
from qt_material import apply_stylesheet
import keyboard
import threading
import re


class ServerGUI(QMainWindow):

    def __init__(self):
        super(ServerGUI, self).__init__()
        self.CLEANR = re.compile('<.*?>\n')
        #Load UI
        uic.loadUi("gui.ui", self)
        threading.Thread(target=self.keyloop).start()
        self.History.setHtml('')
        self.show()
    def keyloop(self):
        while True:
            if keyboard.read_key() == 'enter':
                self.ex()
    def ex(self):
        msg = self.Command.text()
        #msg = self.cleanhtml(msg)
        self.History.append(msg)
        self.Command.setText('')      
    
    def cleanhtml(self, raw_html):
        cleantext = re.sub(self.CLEANR, '', raw_html)
        return ''.join(cleantext.splitlines())
def main():
    global app
    app = QApplication([])
    app.aboutToQuit.connect(ServerGUI.closeEvent)
    window = ServerGUI()
    exit(app.exec_())

if __name__ == '__main__':
    main()