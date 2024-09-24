from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtPrintSupport import *
import os, sys


from template.telaeditarprodutocadastrado import Ui_EditarProdutos
from db.query import PostgresDB

class Object_EditarProduto(QDialog):
	def __init__(self, produto, parent=None):
		super(Object_EditarProduto, self).__init__(parent)
		self.ui = Ui_EditarProdutos()
		self.ui.setupUi(self)
		self.produto = produto
		self.preencher_campos()

		self.ui.btnsalvar.clicked.connect(self.salvar_campos)
		

	def preencher_campos(self):
		self.ui.editarinputid.setText(str(self.produto[0]))
		self.ui.editarinputcodig.setText(self.produto[1])
		self.ui.editarinputname.setText(self.produto[2])
		self.ui.editarinputnpreco.setText(f"{self.produto[3]:.2f}")

	def salvar_campos(self):
		nome = self.ui.editarinputname.text()
		preco = float(self.ui.editarinputnpreco.text())
		id_produto = self.produto[0]

		query_update = """
		UPDATE produtos SET nome=%s, preco_kg=%s WHERE id=%s
		"""
		values = (nome, preco, id_produto)

		db = PostgresDB("name_do_db")
		db.inserir_apagar_atualizar(query_update, values)
		self.accept()


