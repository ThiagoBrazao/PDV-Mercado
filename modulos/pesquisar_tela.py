from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtPrintSupport import *
import os, sys

import csv
from template.telapesquisar import Ui_Pesquisar
from modulos.editarpagcliente_tela import Object_EditarPagamentoClienteFiado
from db.query import PostgresDB



class Object_pesquisar(QDialog):
	def __init__(self, *args, **argvs):
		super(Object_pesquisar, self).__init__(*args, **argvs)
		self.ui = Ui_Pesquisar()
		self.ui.setupUi(self)
		self.ui.btnpesquisar.clicked.connect(self.Pesquisar_Cliente)
		self.ui.btneditar.clicked.connect(self.EditarPagamento)
		self.ui.btnlimpar.clicked.connect(self.add_limpar_pesq)
		self.ui.btnexcluir.clicked.connect(self.Atualizar_campos)
		self.CarregarTabela()
		
		
		#self.setWindowIcon(QIcon('icons/nome_doicon.jpg'))  Comando para alterar o icone da tela em cima!
		


	def Pesquisar_Cliente(self):
		db = PostgresDB("name_do_db")
		valor_consulta = ""
		valor_consulta = self.ui.inputpesq.text().strip() # Remover espaços em branco no início e no fim
		
		# Realizar a consulta no banco de dados com filtro para tipo de venda "À PRAZO"
		query = f"""
		SELECT id, nome, telefone, tipo_venda, data_venda, valor_total
		FROM vendas_prod
		WHERE (nome LIKE '%{valor_consulta}%' OR telefone LIKE '%{valor_consulta}%')
		AND tipo_venda = 'À PRAZO'
		"""
		lista = db.pega_dados(query)
		lista = list(lista)

		# Verificar se a lista está vazia ou se o campo de texto está vazio
		if not lista or not valor_consulta: 
			QMessageBox.warning(QMessageBox(), "Atenção!", "Clíente não tem cadastro!") 
			#self.CarregarTabela()  # Recarregar a tabela com todos os dados
			return
		# Limpar a tabela antes de inserir novos dados
		else:
			self.ui.tablefiados.setRowCount(0) 
		# Inserir os dados na tabela
		for idxLinha, linha in enumerate(lista):
			self.ui.tablefiados.insertRow(idxLinha)
			for idxColuna, coluna in enumerate(linha):
				self.ui.tablefiados.setItem(idxLinha, idxColuna, QTableWidgetItem(str(coluna)))
		self.Salvar_Dados_CSV()  # Salvar os dados no arquivo CSV após a pesquisa
		self.filtrar_e_somar_valores()


	def CarregarTabela(self):
		db = PostgresDB("name_do_db")
		
		query = """
		SELECT id, nome, telefone, tipo_venda, data_venda, valor_total 
		FROM vendas_prod
		WHERE tipo_venda = 'À PRAZO'
		"""
		lista = db.pega_dados(query)
		lista = lista[-13:]
		lista.reverse()
		
		self.ui.tablefiados.setRowCount(0)
		for linha, dados in enumerate(lista):
			self.ui.tablefiados.insertRow(linha)
			for coluna_n, dados in enumerate(dados):
				self.ui.tablefiados.setItem(linha, coluna_n, QTableWidgetItem(str(dados)))
		self.filtrar_e_somar_valores()
		self.Salvar_Dados_CSV()  # Salvar os dados no arquivo CSV após carregar a tabela


	def filtrar_e_somar_valores(self):
		nome_cliente = self.ui.inputpesq.text().strip().lower()
		total = 0 
		for linha in range(self.ui.tablefiados.rowCount()): 
			nome_item = self.ui.tablefiados.item(linha, 1) # Coluna nome do cliente
			valor_item = self.ui.tablefiados.item(linha, 5) # Coluna valor_total
			if nome_item is not None and valor_item is not None:
				nome = nome_item.text().strip().lower()
				if nome_cliente in nome:
					try:
						valor = float(valor_item.text())
						total += valor
					except ValueError:
						print(f"Valor invárlido na linha {linha}: {valor_item.text()}")

		self.ui.somavalores.setText(f"{total:.2f}")


	def EditarPagamento(self):
		linha = self.ui.tablefiados.currentRow()
		if linha == -1:
			print("Nenhuma linha selecionada.")
			return
		
		# Pegar os dados da linha selecionada na tabela
		valor_id = self.ui.tablefiados.item(linha, 0).text()
		nome = self.ui.tablefiados.item(linha, 1).text()
		telefone = self.ui.tablefiados.item(linha, 2).text()
		tipo_venda = self.ui.tablefiados.item(linha, 3).text()
		data_venda = self.ui.tablefiados.item(linha, 4).text()
		valor_total = self.ui.tablefiados.item(linha, 5).text()
		# Criar um dicionário ou lista com os dados do cliente
		cliente = (valor_id, nome, telefone, tipo_venda, data_venda, valor_total)
		# Abrir a tela de edição com os dados do cliente
		editar = Object_EditarPagamentoClienteFiado(cliente, self)
		if editar.exec_() == QDialog.Accepted:
			self.Salvar_Dados_CSV() # Salvar os dados no arquivo CSV após a edição
			#self.CarregarTabela()
			self.filtrar_e_somar_valores() # Atualizar a soma dos valores

		
	def add_limpar_pesq(self):
		self.ui.tablefiados.clearContents()
		self.ui.inputpesq.clear()
		self.CarregarTabela()


	def Atualizar_campos(self):
		nome_cliente = self.ui.inputpesq.text().strip().lower()
		if nome_cliente == "":
			self.CarregarTabela()
		else:
			self.Pesquisar_Cliente()
			self.filtrar_e_somar_valores()
				


	def Salvar_Dados_CSV(self):
		# Nome do arquivo CSV
		arquivo = "dados_fiado.csv"
		# Abrir o arquivo em modo de escrita!
		with open(arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
			escritor_csv = csv.writer(arquivo_csv)
			# Escrever o cabeçalho!
			for linha in range(self.ui.tablefiados.rowCount()):
				dados_linha = []
				for coluna in range(self.ui.tablefiados.columnCount()):
					item = self.ui.tablefiados.item(linha, coluna)
					dados_linha.append(item.text() if item is not None else"")
				escritor_csv.writerow(dados_linha)

