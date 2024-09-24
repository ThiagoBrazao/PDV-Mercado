from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtPrintSupport import *
import os, sys


from template.telacadastro import Ui_Cadastrar
from db.query import PostgresDB

class Object_cadastrar(QDialog):
	def __init__(self, carregadados, *args, **argvs):
		super(Object_cadastrar, self).__init__(*args, **argvs)
		self.ui = Ui_Cadastrar()
		self.ui.setupUi(self)
		self.ui.btnadd.clicked.connect(self.add_cadastro)
		self.ui.btncancel.clicked.connect(self.add_cancelar)
		self.ui.btnlimp.clicked.connect(self.add_limpar)
		self.carrega_dados = carregadados

		quit = QtWidgets.QAction("Quit", self)
		quit.triggered.connect(self.closeEvent)


	def closeEvent(self, event):
		self.carrega_dados()	


	def add_cadastro(self):
		db = PostgresDB("name_do_db")

		name = self.ui.inputname.text()
		phone = self.ui.inputtel.text()
		end = self.ui.inputend.text()
		if name == "" or phone =="" or end =="":
			QMessageBox.information(QMessageBox(), "OPA OPA", "Preencha todos os campos!")
		else:
			query = """
            INSERT INTO cliente_funcio (nome, telefone, endereco)
            VALUES (%s, %s, %s)"""
			values = (name, phone, end)
			db.inserir_apagar_atualizar(query, values)
			QMessageBox.information(QMessageBox(), "Cadastro Realizado!", "CADASTRO REALIZADO COM SUCESSO!")


	def add_cancelar(self):
		self.close()

	
	def add_limpar(self):
		self.ui.inputname.setText("")
		self.ui.inputtel.setText("")
		self.ui.inputend.setText("")
