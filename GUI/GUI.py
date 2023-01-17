#IMPORT
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt, QFile, QTextStream
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon
from qt_material import apply_stylesheet
import base64
import socket
import threading
import requests
import os
import re
from getpass import getuser
import keyboard
#Define Main Class
class MyGui(QMainWindow):
    def __init__(self):
        super(MyGui, self).__init__()
        #Load UI
        uic.loadUi("gui.ui", self)
        #Set Variables
        self.logged_in = False
        #HTML Filter regex
        self.CLEANR = re.compile('<.*?>')
    
        self.connected = False
        self.recv_running = True
        self.api_url = 'http://localhost/'
        self.api_token = 'e112f91bee76c42d9d1e07de3d2ce85aae786189c554ca3d1e043ccf77e32230'
        #Show and configure GUI
        self.show()
        self.setFixedSize(483, 575)
        self.setWindowTitle('Chat Client (BETA)')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.Messages.acceptRichText()
        self.Messages.setOpenExternalLinks(True)

        self.debugbutton.clicked.connect(self.debug)
        self.SendButton.clicked.connect(self.write)
        self.LoginButton.clicked.connect(self.login)
        self.LogoutButton.clicked.connect(self.logout)
        self.ConnectButton.clicked.connect(self.connect)
        self.ReloadButton.clicked.connect(self.scan_server_list_threaded)
        self.DisconnectButton.clicked.connect(self.disconnectb)
        self.LogoutButton.setDisabled(True)
        self.SignUpButton.clicked.connect(self.createAccount)
        self.ServerListBox.activated.connect(self.server_list_connect)
        self.ServerListBox.addItem(QIcon('error.png'), 'Connecting...')
        self.watch_key = threading.Thread(target=self.keyloop)
        self.watch_key.start()
        threading.Thread(target=self.scan_server_list, daemon=True).start()

    def debug(self):
        if self.Messages.isEnabled():
            self.Messages.setDisabled(True)
        else:
            self.Messages.setDisabled(False)
    def scan_server_list_threaded(self):
        threading.Thread(target=self.scan_server_list, daemon=True).start()
    def keyloop(self):
        while True:
            if keyboard.read_key() == 'enter':
                if self.connected:
                    self.write()
    def logout(self):
        self.logged_in == False
        self.LogoutButton.setDisabled(True)
        self.LoginButton.setDisabled(False)
        self.disconnectb()
        self.Messages.setText('')
    
    def closeEvent(self, event):
        exit()

    def server_list_connect(self):
        not self.first
        option = self.ServerListBox.currentText()
        try:
            index = self.serverlist.index(option)
            response = requests.get(f'{self.api_url}getserver/{index+1}', timeout=2).json()
            print(response)
            self.IpBox.setText(response[0])
            self.PortBox.setText(str(response[1]))
            
        except:
            msg = QErrorMessage()
            msg.setWindowIcon(QtGui.QIcon('error.png'))
            msg.setWindowTitle('Connection Error')
            msg.showMessage('There was a problem getting the information for that server. Try again later.')
            return
        
        



    def scan_server_list(self):
        self.ServerListBox.clear()
        self.ServerListBox.addItem('Connecting...')
        try:
            self.serverlist = requests.get(f'{self.api_url}serverlist').json()
        except:
            error = QtGui.QIcon('error.png')
            self.ServerListBox.clear()
            self.ServerListBox.addItem(error, 'Servers unreachable')
            self.ServerListBox.setCurrentText('Servers unreachable')
            return
        self.first = True
        self.ServerListBox.clear()
        self.ServerListBox.addItems(self.serverlist)
    def connect(self):        
        if not self.logged_in:
            msg = QErrorMessage()
            msg.showMessage('Error: Not logged in!')
            return
        try:
            ip = self.IpBox.text()
            port = int(self.PortBox.text())
        except:
            return
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))
        self.connected = True
        self.ConnectButton.setDisabled(True)
        self.DisconnectButton.setDisabled(False)
        self.MsgBox.setDisabled(False)
        self.SendButton.setDisabled(False)
        self.Messages.setDisabled(False)
        self.recv_thread = threading.Thread(target=self.recv, daemon=True)
        self.recv_thread.start()
    def disconnectb(self):
        self.Messages.setText('')
        self.MsgBox.setDisabled(True)
        self.SendButton.setDisabled(True)
        self.ConnectButton.setDisabled(False)
        self.DisconnectButton.setDisabled(True)
        self.recv_running = False
        self.connected = False
        try:
            self.client.close()
        except:
            pass
    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Escape:
            self.close()
            exit()
    def cleanhtml(self, raw_html):
        cleantext = re.sub(self.CLEANR, '', raw_html)
        return cleantext
    def login(self):
        while True:
            try:
                
                self.USERNAME, ok = QInputDialog.getText(self, 'Name', 'Enter your name:')
                if ok != True:
                    break
                self.PASSWORD, ok2 = QInputDialog.getText(self, 'Password', 'Enter your password:', echo=QLineEdit.EchoMode.Password)
                if ok2 != True:
                    break
                if self.USERNAME == None or '':
                    break
                if self.PASSWORD == None or '':
                    break
                request = requests.get(f'{self.api_url}auth/{self.api_token}', json={'user': self.USERNAME, 'password': self.PASSWORD})
                response = request.json()
                user_correct = response['user']
                pass_correct = response['password']
                passfailed = False
                userfailed = False 
                if not user_correct:
                    userfailed = True
                if not pass_correct:
                    passfailed = True
                if passfailed and userfailed == True:
                    msg = QErrorMessage()
                    msg.showMessage('Wrong Username and/or Password.')
                    self.login()
                else:
                    msg = QMessageBox()
                    msg.setText('Logged in!')
                    self.logged_in = True
                    self.LogoutButton.setDisabled(False)
                    self.LoginButton.setDisabled(True)
                    msg = QMessageBox()
                    goated_with_the_sauce = msg.question(self, 'Save Password?', 'Save password for next time?', msg.Yes | msg.No)
                    if not goated_with_the_sauce:
                        pass
                    if goated_with_the_sauce:
                        if not os.path.exists('C:/Python_Chat_Creds/'):
                            os.mkdir('C:/Python_Chat_Creds/')
                        with open(os.path.join('C:/Python_Chat_Creds/', f'Python_Chat_{getuser()}.txt'), 'wb') as f:
                            f.write(f'{[self.USERNAME, self.PASSWORD]}'.encode())
                            msg = QMessageBox()
                            msg.setText('Done!')
                    break
            except:
                msg = QErrorMessage()
                msg.setWindowTitle('Authentication Error.')
                msg.showMessage('Auth servers are unreachable. (Check wifi and internet connection?)')
                break

    def write(self):
        try:
            self.connected
            msg = self.MsgBox.text()
            msg = self.cleanhtml(msg)
            self.client.send(msg.encode())
            self.MsgBox.setText('')
        except:
            msg = QMessageBox()
            msg.setWindowTitle('You were disconnected')
            msg.setText('You were disconnected from the server')
            msg.show()
            self.disconnectb()
    def recv(self):
        self.client.send(self.USERNAME.encode())
        while self.recv_running:
            try:
                msg = self.client.recv(2048).decode()
                msg = self.cleanhtml(msg)
                if msg == '!check':
                    continue
                if msg == 'USERNAME':
                    continue
                print(msg)
                self.Messages.append(msg)

            except:
                pass
    def createAccount(self):
        username, ok = QInputDialog.getText(self, 'Sign Up', 'Username')
        if not ok:
            return
        password, ok = QInputDialog.getText(self, 'Sign Up', 'Password', echo=QLineEdit.EchoMode.Password)
        if not ok:
            return
        confirm_password, ok = QInputDialog.getText(self, 'Sign Up', 'Confirm Password', echo=QLineEdit.EchoMode.Password)
        if not ok:
            return
        if password != confirm_password:
            msg = QErrorMessage(self)
            msg.setWindowTitle('Passwords dont match')
            msg.setWindowIcon(QtGui.QIcon('error.png'))
            msg.showMessage('Passwords do not match!')
            msg.show()
            return
        try:
            print(username)
            print(password)
            self.createAccountResponse = requests.get(f'{self.api_url}register_user/', json={'user': username, 'password': password}).json()
            print(self.createAccountResponse)
        except:
            msg = QErrorMessage()
            msg.setWindowTitle('Authentication Error.')
            msg.showMessage('Auth servers are unreachable. (Check wifi and internet connection?)')
            return
        msg = QMessageBox(self)
        msg.setWindowTitle('Sign Up')
        msg.setText(f'Your Username is: {self.createAccountResponse["user"]}\nand your password is {password}')
        self.USERNAME = self.createAccountResponse["user"]
        self.logged_in = True
        msg.show()

def main():
    global app
    app = QApplication([])
    app.aboutToQuit.connect(MyGui.closeEvent)
    window = MyGui()
    exit(app.exec_())

if __name__ == '__main__':
    main()