import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap
import sqlite3
class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi('w.ui', self)
        self.login.clicked.connect(self.gotologin)
        self.create.clicked.connect(self.gotocreate)
    
    def gotologin(self):
        print('a')
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotocreate(self):
        create = CreateAccount()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex()+1)
class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi('login.ui', self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.login.clicked.connect(self.loginfunc)

    def loginfunc(self):
        user = self.usernamefield.text()
        password = self.passwordfield.text()

        if len(user) ==0 or len(password) == 0:
            self.error.setText("Please Input all fields!")

        else:
            conn = sqlite3.connect("shop_data.db")
            cur = conn.cursor()
            query = 'SELECT password FROM login_info WHERE username =\''+user+"\'" 
            cur.execute(query)
            try:
                result_pass = cur.fetchone()[0]
            except TypeError:
                self.error.setText("Invalid Username or password")
                return
            if result_pass == password:
                print('Succesfully logged in!')
            else:
                self.error.setText('Invalid Username or password')
        
class CreateAccount(QDialog):
    def __init__(self):
        super(CreateAccount, self).__init__()
        loadUi('createacc.ui', self)    
        self.create.clicked.connect(self.signup)

    def signup(self):
        user = self.username.text()
        password = self.password.text()
        confirmpassword = self.confirmpassword.text()

        if len(user) == 0 or len(password) == 0 or len(confirmpassword) == 0:
            self.error.setText("Please fill in all fields")
        
        elif password != confirmpassword:
            self.error.setText('Passwords do not match')

        else:
            conn = sqlite3.connect('shop_data.db')
            cur = conn.cursor()

            user_info = [user, password]
            cur.execute('INSERT INTO login_info (username, password) VALUES (?,?)', user_info)

            conn.commit()
            conn.close()


            fillprofile = FillProfileScreen()
            widget.addWidget(fillprofile)
            widget.setCurrentIndex(widget.currentIndex()+1)

class FillProfileScreen(QDialog):
    def __init__(self):
        super(FillProfileScreen, self).__init__()
        loadUi('fillprofile.ui', self)
        self.image.setPixmap(QPixmap('placeholder.png'))
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()

try:
    sys.exit(app.exec())
except:
    exit()