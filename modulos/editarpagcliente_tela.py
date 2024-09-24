from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtPrintSupport import *
import os, sys


from template.telacontrolepaga import Ui_ControlePagamen
from db.query import PostgresDB

class Object_EditarPagamentoClienteFiado(QDialog):
	def __init__(self, cliente, parent=None):
		super(Object_EditarPagamentoClienteFiado, self).__init__(parent)
		self.ui = Ui_ControlePagamen()
		self.ui.setupUi(self)
		self.cliente = cliente
		self.mostrar_campos()
		self.ui.btnsalvar.clicked.connect(self.salvar_campos)
	
	def mostrar_campos(self):
		self.ui.inputid.setText(str(self.cliente[0]))
		self.ui.inputnome.setText(str(self.cliente[1]))
		self.ui.inputtelefone.setText(str(self.cliente[2]))
		self.ui.inputtipoven.setText(str(self.cliente[3]))
		self.ui.inputdatetime.setText(str(self.cliente[4]))
		self.ui.inputpreco.setText(str(self.cliente[5]))
	
	def salvar_campos(self):
		# name = self.ui.inputid.text()
		# tel = self.ui.inputtelefone.text()
		valorTotal = float(self.ui.inputpreco.text())
		id_cliente = self.cliente[0]

		query_update = """
		UPDATE vendas_prod SET valor_total=%s WHERE id=%s
		AND tipo_venda = 'À PRAZO'
		"""
		values = (valorTotal, id_cliente)

		db = PostgresDB("name_do_db")
		db.inserir_apagar_atualizar(query_update, values)
		self.accept()

