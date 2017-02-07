from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from MainWindow import Ui_Gerador
import sys
import csv
import subprocess
import os
import time


class Gerador(QMainWindow):
    def __init__(self, parent=None):
        self.modelo = ''
        self.participantes = ''
        self.saida = ''
        super(Gerador, self).__init__()
        self.ui = Ui_Gerador()
        self.ui.setupUi(self)
        self.ui.abrir_modelo.clicked.connect(self.abrir_modelo)
        self.ui.actionModelo.triggered.connect(self.abrir_modelo)
        self.ui.abrir_participantes.clicked.connect(self.abrir_participantes)
        self.ui.actionParticipantes.triggered.connect(self.abrir_participantes)
        self.ui.abrir_saida.clicked.connect(self.abrir_saida)
        self.ui.gerar_certificado.clicked.connect(self.gerar_certificados)

    def __del__(self):
        self.clear_files()

    def abrir_modelo(self):
        self.modelo = QFileDialog().getOpenFileName(caption='Carregar modelo (.tex)', filter='*.tex')
        if self.modelo:
            self.modelo = self.modelo[0]
            self.ui.lineEdit.setText(self.modelo)

    def abrir_participantes(self):
        self.participantes = QFileDialog().getOpenFileName(caption='Carregar participantes (.csv)', filter='*.csv')
        if self.participantes:
            self.participantes = self.participantes[0]
            self.ui.lineEdit_2.setText(self.participantes)

    def abrir_saida(self):
        self.saida = QFileDialog().getExistingDirectory(caption='Escolha a pasta de saída')
        if self.saida:
            self.ui.lineEdit_3.setText(self.saida)

    def gerar_certificados(self):
        if self.modelo and self.participantes and self.saida:
            with open(self.modelo) as arq:
                tx = arq.read()
            with open(self.participantes) as f:
                leitor = csv.reader(f)
                next(leitor)
                for linha in leitor:
                    ID = linha[0]
                    data = linha[1]
                    Cr = linha[2]
                    Cg = linha[3]
                    saida = tx % (ID, Cr, data, Cg)
                    arq_name =  self.saida+'/' + ID + '.tex'
                    TexFile = open(arq_name, 'w')
                    TexFile.write(saida)
                    TexFile.close()
                    p = subprocess.Popen(['pdflatex', arq_name], shell=False, stdout=subprocess.DEVNULL)
                    self.ui.arquivos_processados.addItem(ID)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText('Erro ao processar! Arquivo nao selecionado')
            msg.setWindowTitle('Erro')
            msg.exec_()

    def clear_files(self):
        os.system('rm *.aux *.log')
        os.system('mv *.pdf Certificados')


app = QApplication(sys.argv)
form = Gerador()
form.show()
app.exec_()
