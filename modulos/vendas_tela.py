from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtPrintSupport import *
import os, sys

# from escpos.printer import Usb  #Quando comprar a IMPRESSORA!


from template.telavendaprod import Ui_TelaVendas
from db.query import PostgresDB
from PyQt5.QtCore import QDateTime
from PyQt5.QtCore import pyqtSignal



class Object_vendas(QDialog):
	proximo_code = 1  # Atributo de classe para armazenar o próximo código disponível
	codigos_usados = set() # Conjunto para armazenar os códigos usados
	def __init__(self, parent=None, usertelavendas=None, usertelefonetelavendas=None, tipovenda=None):
		super(Object_vendas, self).__init__(parent)
		self.ui = Ui_TelaVendas()
		self.ui.setupUi(self)
		self.tipovenda = tipovenda
		
		self.inputcod = Object_vendas.proximo_code  # Atribui o próximo código disponível
		Object_vendas.proximo_code += 1
		self.ui.inputcod.setText(str(self.inputcod)) # Exibe o código no QLineEdit

		# Mostar o usuário e telefone conectado na tela_vendas_produtos!
		self.usertelavendas = usertelavendas
		self.usertelefonetelavendas = usertelefonetelavendas
		
		# Aqui são os botões e input da tela_vendas!
		self.ui.user_conect_user.setText(self.usertelavendas)
		self.ui.inputnome.setText(self.usertelavendas)
		self.ui.inputtelefo.setText(self.usertelefonetelavendas)

		self.ui.btnfinalizar_2.clicked.connect(self.finalizar_pedido)
		self.ui.btnregistrar.clicked.connect(self.adicionar_item)
		self.ui.btnlimpar.clicked.connect(self.add_limpar_dados)
		
		self.ui.btnimprimir.clicked.connect(self.finalizar_pedido)

		# Configura o QDateTimeEdit para pegar a data e hora atuais
		self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())

		# Carrega o tipo de carne no QCombox da tela_vendas_prod
		self.CarregarTipo_carne()
		self.ui.listadeTcarne.currentIndexChanged.connect(self.atualizar_valor_por_quilo)


	def add_limpar_dados(self):
		self.ui.inputcod.clear()
		self.ui.inputnome.clear()
		self.ui.inputtelefo.clear()
		self.ui.listadeTcarne.setCurrentIndex(0)
		self.ui.precokg.clear()
		self.ui.qntquilos.clear()
		self.ui.precototalparcial.clear()
		self.ui.dateTimeEdit.clear()
		self.ui.radiobutton_dinheiro.setChecked(False)
		self.ui.radiobutton_debito.setChecked(False)
		self.ui.radiobutton_credito.setChecked(False)
		self.ui.radiobutton_fiado.setChecked(False)


	def set_tipo_venda(self, tipovenda):
		if tipovenda == "DINHEIRO":
			self.ui.radiobutton_dinheiro.setChecked(True)
		elif tipovenda == "DÉBITO":
			self.ui.radiobutton_debito.setChecked(True)
		elif tipovenda == "CRÉDITO":
			self.ui.radiobutton_credito.setChecked(True)
		elif tipovenda == "À PRAZO": 
			self.ui.radiobutton_fiado.setChecked(True)  # Supondo que este seja o radio button para "À Prazo"


	def CarregarTipo_carne(self):
		try:
			db = PostgresDB("name_do_db")
			
			query = """
			SELECT nome, preco_kg FROM produtos
			"""
			dados = db.pega_dados(query)
			for tipo in dados:
				self.ui.listadeTcarne.addItem(tipo[0], tipo[1])
		except Exception as e:
			QMessageBox.warning(self, "Algo deu errado!", f"Tente novamente! Erro:{str(e)}")

		
	def atualizar_valor_por_quilo(self):
		valor_por_quilo = self.ui.listadeTcarne.currentData()
		if valor_por_quilo is not None:
			self.ui.precokg.setValue(float(valor_por_quilo))


	def adicionar_item(self):
		codig = self.ui.inputcod.text()
		name = self.ui.inputnome.text()
		phone = self.ui.inputtelefo.text()
		listaCarne = self.ui.listadeTcarne.currentText()
		precokg = self.ui.precokg.value()
		qntkg = self.ui.qntquilos.value()
		preco_parcial = float(precokg) * float(qntkg)
		dateTime = self.ui.dateTimeEdit.text()
    
		self.tipovenda = ""
		if self.ui.radiobutton_dinheiro.isChecked():
			self.tipovenda = "DINHEIRO"
		elif self.ui.radiobutton_debito.isChecked():
			self.tipovenda = "DÉBITO"
		elif self.ui.radiobutton_credito.isChecked():
			self.tipovenda = "CRÉDITO"
		elif self.ui.radiobutton_fiado.isChecked():
			self.tipovenda = "À PRAZO"
		
		
		if codig == "" or name == "" or phone == "" or precokg == 0 or qntkg == 0 or  not self.tipovenda:
			QMessageBox.information(self, "OBSERVAÇÃO", "Preencha todos os campos obrigatórios!")
			return

		# Verifique se o código já foi usado
		if codig in Object_vendas.codigos_usados:
			QMessageBox.information(self, "OBSERVAÇÃO", "O código já foi usado! Por favor, gere um novo código.")
			return
		
		# Adicione o código ao conjunto de códigos usados
		Object_vendas.codigos_usados.add(codig)

		linha = self.ui.tablepedidos.rowCount()
		self.ui.tablepedidos.insertRow(linha)
		self.ui.tablepedidos.setItem(linha, 0, QTableWidgetItem(codig))
		self.ui.tablepedidos.setItem(linha, 1, QTableWidgetItem(name))
		self.ui.tablepedidos.setItem(linha, 2, QTableWidgetItem(phone))
		self.ui.tablepedidos.setItem(linha, 3, QTableWidgetItem(listaCarne))
		self.ui.tablepedidos.setItem(linha, 4, QTableWidgetItem(str(precokg)))
		self.ui.tablepedidos.setItem(linha, 5, QTableWidgetItem(str(qntkg)))
		self.ui.tablepedidos.setItem(linha, 6, QTableWidgetItem(str(preco_parcial)))
		self.ui.tablepedidos.setItem(linha, 7, QTableWidgetItem(dateTime))
		self.ui.tablepedidos.setItem(linha, 8, QTableWidgetItem(self.tipovenda))
		self.ui.tablepedidos.setItem(linha, 9, QTableWidgetItem(str(preco_parcial)))
		
		
		self.atualizar_total_pedido()
		

	def atualizar_total_pedido(self):
		total_pedido = 0
		for linha_p in range(self.ui.tablepedidos.rowCount()):
			item_preco_total = self.ui.tablepedidos.item(linha_p, 6)
			preco_total = float(item_preco_total.text()) if item_preco_total is not None else 0.0
			total_pedido += preco_total
		
		self.ui.precototalparcial.setText(f"R$ {total_pedido:.2f}")
		self.ui.valorTotal.setText(f"R$ {total_pedido:.2f}")



	def finalizar_pedido(self):
		db = PostgresDB("name_do_db")
		total_pedido = 0

		# Configurar a impressora (substitua os valores de idVendor e idProduct pelos da sua impressora)
    	#p = Usb(0x04b8, 0x0e15)

			#p.text("Recibo de Venda\n")
			#p.text("----------------------------\n")

		print("Recibo de Venda\n")
		print("----------------------------\n")
		
		for linha_p in range(self.ui.tablepedidos.rowCount()):
			item_codig = self.ui.tablepedidos.item(linha_p, 0)
			codig = item_codig.text() if item_codig is not None else ""
        
			item_name = self.ui.tablepedidos.item(linha_p, 1)
			name = item_name.text() if item_name is not None else ""
		
			item_phone = self.ui.tablepedidos.item(linha_p, 2)
			phone = item_phone.text() if item_phone is not None else ""
		
			item_listaCarne = self.ui.tablepedidos.item(linha_p, 3)
			listaCarne = item_listaCarne.text() if item_listaCarne is not None else ""
		
			item_precokg = self.ui.tablepedidos.item(linha_p, 4)
			precokg = float(item_precokg.text()) if item_precokg is not None else 0.0
		
			item_qntkg = self.ui.tablepedidos.item(linha_p, 5)
			qntkg = float(item_qntkg.text()) if item_qntkg is not None else 0.0
		
			item_preco_total = self.ui.tablepedidos.item(linha_p, 6)
			preco_total = float(item_preco_total.text()) if item_preco_total is not None else 0.0
		
			item_dateTime = self.ui.tablepedidos.item(linha_p, 7)
			dateTime = item_dateTime.text() if item_dateTime is not None and item_dateTime.text() != "" else None

			item_tipovenda = self.ui.tablepedidos.item(linha_p, 8)
			self.tipovenda = item_tipovenda.text() if item_tipovenda is not None else ""
        
			item_vTotal = self.ui.tablepedidos.item(linha_p, 9)
			vTotal = float(item_vTotal.text()) if item_vTotal is not None and item_vTotal.text() != "" else None
        
			total_pedido += preco_total
		
			query = """
			INSERT INTO vendas_prod (codigo, nome, telefone, tipo_carne, preco_kg, qnt_kg, preco_parcial, data_venda, tipo_venda, valor_total)
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
			"""
			values = (codig, name, phone, listaCarne, precokg, qntkg, preco_total, dateTime, self.tipovenda, vTotal)
			db.inserir_apagar_atualizar(query, values)
		
		# Adicionar informações ao recibo
		print(f"Código: {codig}\n")
		print(f"Nome: {name}\n")
		print(f"Telefone: {phone}\n")
		print(f"Tipo de Carne: {listaCarne}\n")
		print(f"Preço por Kg: R$ {precokg:.2f}\n")
		print(f"Quantidade (Kg): {qntkg:.2f}\n")
		print(f"Preço Total: R$ {preco_total:.2f}\n")
		print("----------------------------\n")

		print(f"Total do Pedido: R$ {total_pedido:.2f}\n")
		#p.cut()

		self.ui.valorTotal.setText(f"R$ {total_pedido:.2f}")
		QMessageBox.information(self, "Pedido Finalizado", f"Total do Pedido: R$ {total_pedido:.2f}")
		self.ui.tablepedidos.setRowCount(0)  # Limpa a tabela após finalizar o pedido
	