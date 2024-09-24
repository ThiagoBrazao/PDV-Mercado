from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtPrintSupport import *
import os, sys


from modulos.principal_tela import Object_telaprincipal
from template.telalogin import Ui_Login
from db.query import PostgresDB

class Object_login(QDialog):


	def __init__(self,*args,**argvs):
		super(Object_login,self).__init__(*args,**argvs)
		self.ui = Ui_Login()
		self.ui.setupUi(self)
		self.ui.btnentrar.clicked.connect(self.login)
		
			
	def login(self):
		db = PostgresDB("name_do_db")

		user = self.ui.namedouser.text().strip().lower()
		passwd = self.ui.passwduser.text()
		if user == " " or passwd == " ":
			QMessageBox.information(QMessageBox(), "Alerta!", "Preencha todos os campos!!")
		else:	
			query = "SELECT * FROM users WHERE username = %s AND passwd = %s"
			dados = db.pega_dados(query, (user, passwd))
			if dados:
				QMessageBox.information(QMessageBox(), "Login Realizado!", "Acesso Realizado com Sucesso!")
				self.userlogado = user
				self.window = Object_telaprincipal(self, self.userlogado)
				self.window.show()
				self.hide()   #Fecha a teladologin!
			else:
				QMessageBox.warning(QMessageBox(), "Login falhou!", "Login ou Senha Incorretos. Tente novamente!")	
		
	
	def clearInputs(self): # Limpa os dados quando a tela de login abre após a principal ser fechada!
		self.ui.namedouser.clear()
		self.ui.passwduser.clear()	


	def closeEvent(self, event): 
		reply = QMessageBox.question(self, 'Alerta!', 
								"Tem certeza que deseja sair?", QMessageBox.Yes | 
								QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.Yes:
			event.accept()
			QApplication.quit() #Encerra o Sistema
		else:
			event.ignore()
