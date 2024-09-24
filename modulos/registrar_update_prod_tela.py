from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtPrintSupport import *
import os, sys



from template.telacadastroprod import Ui_TelaRegistra_Produto
from modulos.editarproduto_tela import Object_EditarProduto
from db.query import PostgresDB


class Object_atualizar_cadastrar_produto(QDialog):
	def __init__(self, *args, **argvs):
		super(Object_atualizar_cadastrar_produto, self).__init__(*args, **argvs)
		self.ui = Ui_TelaRegistra_Produto()
		self.ui.setupUi(self)
		self.CarregaDados_TelaCadastroProdutos()
		
		self.ui.btnregistrar.clicked.connect(self.Adicionar_Produto)
		self.ui.btnatualizardados.clicked.connect(self.EditarProdutos)
		self.ui.btnlimpardados.clicked.connect(self.Limpar_Campos)
		self.ui.btnexcluirdados.clicked.connect(self.Apagar_Produtos)
		
		
		
	def Adicionar_Produto(self):
		try:
			db = PostgresDB("name_do_db")

			Cod = self.ui.inputcodp.text()
			Nome = self.ui.inputnamep.text()
			Precokg = self.ui.inputprecokg.text()

			if Cod == "" or Nome == "" or Precokg == "":
				QMessageBox.warning(self, "ATENÇÃO!", "PREENCHA TODOS OS CAMPOS")

			else:
				query = """
				INSERT INTO produtos (codigo, nome, preco_kg)
            	VALUES (%s, %s, %s)"""
				values = (Cod, Nome, Precokg)

				db.inserir_apagar_atualizar(query, values)
				QMessageBox.information(self, "PRODUTOS ADICIONADOS!", "PRODUTOS ADICIONADOS COM SUCESSO!")
			
				self.CarregaDados_TelaCadastroProdutos()
				self.Limpar_Campos()
		except Exception as e:
			QMessageBox.warning(self, "ALGO DEU ERRADO!", f"POR FAVOR, TENTE NOVAMENTE! Erro: {e}")

	
	# To atualizando isso!
	def EditarProdutos(self):
		db = PostgresDB("name_do_db")

		linha = self.ui.tablecadastraeupdateprods.currentRow()
		if linha == -1:
			print("Nenhuma linha selecionada.")
			return
		
		query = """
		SELECT id FROM produtos
		"""
		dados_lidos = db.pega_dados(query)
		
		if linha >= len(dados_lidos):
			print("Linha selecionada fora do intervalo.")
			return
		
		valor_id = dados_lidos[linha][0]
		
		query_select = """
		SELECT * FROM produtos WHERE id=%s
		"""
		values = (valor_id,)
		produtos = db.pega_dados(query_select, values)

		if produtos:
			produto = produtos[0]
			editar = Object_EditarProduto(produto, self)
			if editar.exec_() == QDialog.Accepted:
				self.CarregaDados_TelaCadastroProdutos()
		else:
			print("Produto não encontrado.")
	


	def Limpar_Campos(self):
		codigo = ""
		nome = ""
		precokg = ""
		self.ui.inputcodp.setText(nome)
		self.ui.inputnamep.setText(precokg)
		self.ui.inputprecokg.setText(precokg)


	def Apagar_Produtos(self):
		db = PostgresDB("name_do_db")

		linha = self.ui.tablecadastraeupdateprods.currentRow()
		
		if linha == -1:
			print("Nenhuma linha selecionada.")
			return
		
		self.ui.tablecadastraeupdateprods.removeRow(linha)
		query = """
		SELECT id FROM produtos
		"""
		dados_lidos = db.pega_dados(query)
		
		if linha >= len(dados_lidos):
			print("Linha selecionada fora do intervalo.")
			return
		
		valor_id = dados_lidos[linha][0]
		
		query_delete = """
		DELETE FROM produtos WHERE id=%s
		"""
		values = (valor_id,)
		
		db.inserir_apagar_atualizar(query_delete, values)
		QMessageBox.information(self, "PROTUDO EXCLUÍDO!", "PRODUTO EXCLUÍDO COM SUCESSO!")
		self.CarregaDados_TelaCadastroProdutos()
		#print(f"Produto com ID {valor_id} foi apagado.")
		
	
	def CarregaDados_TelaCadastroProdutos(self):
		db = PostgresDB("name_do_db")
		
		query = "SELECT id, codigo, nome, preco_kg FROM produtos"
		lista = db.pega_dados(query)
		# lista = lista[-7:]
		# lista.reverse()
		
		self.ui.tablecadastraeupdateprods.setRowCount(0)
		for linha, dados in enumerate(lista):
			self.ui.tablecadastraeupdateprods.insertRow(linha)
			for coluna_n, dados in enumerate(dados):
				self.ui.tablecadastraeupdateprods.setItem(linha, coluna_n, QTableWidgetItem(str(dados)))