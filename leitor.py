from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot,Qt,QCoreApplication,QEvent,QDateTime, QTime, QTimer, QObject, QSize
from PyQt5.QtGui import *

import time

from ctypes import c_char_p

from multiprocessing import Process,Lock, cpu_count,current_process,Manager
from leituras import ShowReadings
sr = ShowReadings()

class ReaderCardNfc(QMainWindow):

    def __init__(self):

        self.StyleSheet_consultar = '''
                        QPushButton {border:none;color: #BFBFBF;background-color: #0F7799;border-radius: 5px;padding: 5px;}
                        QPushButton:hover {background-color: #82A6C9;color: #fff;}
                        QPushButton:pressed {color: #F0DEDE; border: 5px solid #658EB7;border-radius: 4px;font-size: 7px}
                        QPushButton:flat { border: 5} 
                '''

        self.root=QMainWindow.__init__(self)
        self.screnn_leitor = loadUi("guis/principal.ui", self)
        self.screnn_leitor.setStyleSheet("background-color:#003A73;")
        self.setWindowFlag(Qt.FramelessWindowHint) #--/[ Remover a barra de titulos ]
        self.screnn_leitor.setWindowTitle("Sistema de leitura NFc")
        self.screnn_leitor.funcionario_textEdit.setEnabled(False)
        self.screnn_leitor.funcionario_textEdit.setText('Jose de Almeida Lobinho')

        self.statusBarra=self.statusBar()
        self.statusBarra.showMessage('   Processos Ativos: Leitura do cartão NFc [ON], Display de duas colunas [ON]')
        self.screnn_leitor.informe_pushButton.setText("Aproxime o Cartão no Leitor")
        self._geometry = QDesktopWidget().screenGeometry() #--[ Valor da geometria {MONITOR} ]
        self._frame = self.screnn_leitor.frameGeometry() #---[ Tamanhdo da frame {TELA-Visivel} ]

        """ Abrir Centralizado """
        cp = QDesktopWidget().availableGeometry().center()
        self._frame.moveCenter(cp)
        self.screnn_leitor.move(self._frame.topLeft())

        """ Abrir em FullScreen """
        #self.showFullScreen()

        timer = QTimer(self)
        timer.timeout.connect(self.past_time)
        timer.start(500)

        self.im = QPixmap("images/logo.png")
        self.screnn_leitor.foto_label.setPixmap(self.im)
        self.screnn_leitor.foto_label.setScaledContents(True)

        #self.screnn_leitor.desligar_leitor_pushButton.clicked.connect(self.lobo)
        self.screnn_leitor.sair_pushButton.clicked.connect(self.exit_app)

        """ Thread """
        self.manager = Manager()
        self.return_read_nfc = self.manager.Value(c_char_p, None)
        self.thread_read_nfc = Process(target=lambda:  sr.read_nfc(self))
        self.thread_read_nfc.start()

        self.definitions()

    def exit_app(self):

        if self.thread_read_nfc:   self.thread_read_nfc.terminate()
        QCoreApplication.instance().quit()

    def past_time(self):

        time = QDateTime.currentDateTime()
        hora = time.toString('hh:mm:ss dd/MM/yyyy')
        self.screnn_leitor.horario_real_label.setText(hora)
        self.screnn_leitor.horario_real_label.setStyleSheet("font: 30px;font-weight: bold;color:#79C4DC;background-color:#002243;border-radius: 5px;")
        self.screnn_leitor.horario_real_label.setAlignment(Qt.AlignCenter)

        default_style = '''
                        QPushButton {border:none;color: #F0F034;background-color: #0F7799;border-radius: 5px;padding: 5px; text-align: left;}
                        QPushButton:hover {background-color: #82A6C9;color: #fff;}
                        QPushButton:pressed {color: #F0DEDE; border: 5px solid #658EB7;border-radius: 4px;font-size: 7px}
                        QPushButton:flat { border: 5} 
                '''

        if self.return_read_nfc.value:
            self.screnn_leitor.informe_pushButton.setText(f" Bem Vindo: {self.return_read_nfc.value}")
            self.screnn_leitor.informe_pushButton.setStyleSheet(default_style)
            self.screnn_leitor.informe_pushButton.setLayoutDirection(Qt.RightToLeft)
        else:
            self.screnn_leitor.informe_pushButton.setText("Aproxime o Cartão no Leitor")
            self.screnn_leitor.informe_pushButton.setStyleSheet(self.StyleSheet_consultar)

        print(self.thread_read_nfc)
        
    def definitions(self):

        self.StyleSheet = '''
                        QPushButton {border:none;background-color: #5D8997;border-radius: 5px;text-align: left; padding: 15px;}
                        QPushButton:hover {background-color: #114252;color: #8DDDF7;}
                        QPushButton:pressed {color: #268EF6; border: 5px solid #1B5E74;border-radius: 8px;}
                        QPushButton:flat { border: 5} 
            '''

        """ Efects """
        sh_b1 = QGraphicsDropShadowEffect()
        sh_b2 = QGraphicsDropShadowEffect()
        sh_b3 = QGraphicsDropShadowEffect()
        sh_b4 = QGraphicsDropShadowEffect()
        sh_b5 = QGraphicsDropShadowEffect()
        sh_b6 = QGraphicsDropShadowEffect()

        self.screnn_leitor.desligar_leitor_pushButton.setStyleSheet(self.StyleSheet_consultar)
        self.screnn_leitor.desligar_display_pushButton.setStyleSheet(self.StyleSheet_consultar)
        self.screnn_leitor.sair_pushButton.setStyleSheet(self.StyleSheet_consultar)
        self.screnn_leitor.informe_pushButton.setStyleSheet(self.StyleSheet_consultar)
        self.screnn_leitor.desligar_leitor_pushButton.setGraphicsEffect(self.shadow(sh_b1))
        self.screnn_leitor.desligar_display_pushButton.setGraphicsEffect(self.shadow(sh_b2))
        self.screnn_leitor.sair_pushButton.setGraphicsEffect(self.shadow(sh_b3))
        self.screnn_leitor.informe_pushButton.setGraphicsEffect(self.shadow(sh_b4))

        """ Texts and labels"""
        self.screnn_leitor.funcionario_textEdit.setStyleSheet("font: 15px;font-weight: bold;color:#79C4DC;background-color:#002243;border-radius: 5px;")
        self.screnn_leitor.funcionario_textEdit.setGraphicsEffect(self.shadow(sh_b6))
        self.screnn_leitor.horario_real_label.setGraphicsEffect(self.shadow(sh_b5))

        """ Labels """
        my_style="font: 15px;font-weight: bold;color:#79C4DC"
        my_style_status_barra="font: 15px;font-weight: bold;color:#919191"
        self.screnn_leitor.data_hora_label.setStyleSheet(my_style)
        self.screnn_leitor.ultima_leitura_label.setStyleSheet(my_style)
        self.screnn_leitor.informe_label.setStyleSheet(my_style)
        self.statusBarra.setStyleSheet(my_style_status_barra)

        self.screnn_leitor.label_versao.setStyleSheet("font-weight: bold;color:#211BC8")
        self.screnn_leitor.foto_label.setStyleSheet("font: 15px;font-weight: bold;color:#79C4DC;background-color:#002243;border-radius: 5px;")

    def shadow(self, objs):

        objs.setBlurRadius(3)
        objs.setXOffset(5)
        objs.setYOffset(5)
        return objs

if __name__ == '__main__':

    app = QApplication([])
    app.setStyle('cleanlooks')
        #['bb10dark', 'bb10bright', 'cleanlooks', 'cde', 'motif', 'plastique', 'Windows', 'Fusion',Breeze', 'Oxygen', 'QtCurve']

    window = ReaderCardNfc()
    window.show()
    app.exec_()