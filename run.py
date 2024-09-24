import sys
from PyQt5.QtWidgets import QDialog, QApplication
from modulos.login_tela import Object_login

app = QApplication(sys.argv)
if (QDialog.Accepted == True):
    window = Object_login()
    window.show()
sys.exit(app.exec_())    
