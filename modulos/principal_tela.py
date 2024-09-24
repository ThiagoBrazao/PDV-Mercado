from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtPrintSupport import *
import os, sys


from template.telaprincipal import Ui_MainWindow
from modulos.cadastrar_tela import Object_cadastrar
from modulos.pesquisar_tela import Object_pesquisar
from modulos.vendas_tela import Object_vendas
from modulos.registrar_update_prod_tela import Object_atualizar_cadastrar_produto
from db.query import PostgresDB


class Object_telaprincipal(QMainWindow):
	def __init__(self, telalogin, userlogado, *args, **argvs):
		super(Object_telaprincipal, self).__init__(*args,**argvs)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		
		self.telalogin = telalogin   # Inicialize outros componentes da tela principal aqui
		
		self.ui.actionProcurar.triggered.connect(self.Open_actionProcurar)
		self.ui.actionPesquisar_2.triggered.connect(self.Open_actionPesquisar)
		self.ui.actionCadastrarProd.triggered.connect(self.Open_actionRegisProdAtualizar)
		self.ui.actionAtualizar.triggered.connect(self.Open_actionAtualizar)
		
		self.click_count = 0  # Inicialize o contador de cliques PARA OS RADIO_BUTTONS
		# Conecte os botões corretamente
		self.ui.actionVendas.triggered.connect(self.handle_button_click)
		self.ui.btndinheiro.clicked.connect(self.handle_button_click)
		self.ui.btncredito.clicked.connect(self.handle_button_click)
		self.ui.btndebito.clicked.connect(self.handle_button_click)
		self.ui.btnfiado.clicked.connect(self.handle_button_click)

		
		self.CarregaDados()
		self.user_logado = userlogado
		self.ui.userconnect1.setText(self.user_logado)

		#Acessar com o nome ou telefone do cliente na tela_principal
		self.ui.pesquisar_cliente.clicked.connect(self.verificarCliente)

		
		
	def closeEvent(self, event): # Fecha a janela atual e reexibe a janela desejada.
		reply = QMessageBox.question(self, 'Alerta!', 
								"Tem certeza que deseja sair?", QMessageBox.Yes | 
								QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.Yes:
			event.accept()
			self.telalogin.clearInputs()
			self.telalogin.show()
			self.clearMask()
			self.destroy()	
		else:
			event.ignore()
			

	def verificarCliente(self):
		db = PostgresDB("name_do_db")
		
		name = self.ui.pesquisarClienteLine.text().strip()
		telefone = self.ui.pesquisarClienteLine.text()

		query = "SELECT nome, telefone FROM cliente_funcio WHERE nome = %s OR telefone = %s"
		dados = db.pega_dados(query, (name, telefone))
		if dados:
			QMessageBox.information(self, "Login Realizado!", "Acesso Realizado com Sucesso!")
			self.usertelavendas = dados[0][0]  #Primeiro 0 é a linha o segundo 0 é coluna, no caso fica linha 0 da coluna 0 = nome
			self.usertelefonetelavendas = dados[0][1]		   #Linha 0 da coluna 1 = telefone	
			self.window = Object_vendas(self, self.usertelavendas, self.usertelefonetelavendas)
			self.window.show()
		else:
			QMessageBox.warning(self, "Login falhou!", "Usuário não cadastrado!")	
			

	
	def Open_actionProcurar(self):
		add = Object_cadastrar(self.CarregaDados)
		add.exec_()	


	def Open_actionPesquisar(self):
		addp = Object_pesquisar()
		addp.exec_()


	def Open_actionVendas(self, tipovenda=None):
		addv = Object_vendas()
		if tipovenda:
			addv.set_tipo_venda(tipovenda)
		addv.exec_()
	

	def Open_actionRegisProdAtualizar(self):
		addrp = Object_atualizar_cadastrar_produto()
		addrp.exec_()

	def Open_actionAtualizar(self):
		addatt = self.CarregaDados()

	def CarregaDados(self):
		db = PostgresDB("name_do_db")
		
		query = """
		SELECT codigo, nome, telefone, tipo_carne, preco_kg, qnt_kg, preco_parcial, data_venda, 
		tipo_venda, valor_total
		FROM vendas_prod
		"""
		lista = db.pega_dados(query)
		lista = lista[-10:]
		lista.reverse()
		
		self.ui.tabelavendas.setRowCount(0)
		for linha, dados in enumerate(lista):
			self.ui.tabelavendas.insertRow(linha)
			for coluna_n, dados in enumerate(dados):
				self.ui.tabelavendas.setItem(linha, coluna_n, QTableWidgetItem(str(dados)))
		

	
	# Chama a função Open_actionVendas para adicionar a tela_vendas com as seguintes condições dos botões!
	def handle_button_click(self):
		opcao = self.sender()
		if opcao == self.ui.btndinheiro:
			tipovenda = "DINHEIRO"
		elif opcao == self.ui.btncredito:
			tipovenda = "CRÉDITO"
		elif opcao == self.ui.btndebito:
			tipovenda = "DÉBITO"
		elif opcao == self.ui.btnfiado:
			tipovenda = "À PRAZO"
		else:
			tipovenda = None
		self.Open_actionVendas(tipovenda)

	# Checar a funcionalidade dos Radio_Button que temos na tela_principal!
	def get_tipo_venda(self):
		if self.ui.radiobutton_dinheiro.isChecked():
			return "DINHEIRO"
		elif self.ui.radiobutton_credito.isChecked():
			return "CRÉDITO"
		elif self.ui.radiobutton_debito.isChecked():
			return "DÉBITO"
		else:
			return "À PRAZO"


	
