#!/usr/sbin/evn python3
# Jose de Almeida Lobino 2020-09-19

# Module Adafruit PN532 RFID/NFC
import board
import busio
import sys
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI
from getkey import getkey, keys

# Module Lcd 16x2 I2c
from libs.lcddriver import lcd

from datetime import datetime
from subprocess import getoutput
from multiprocessing import Process,Lock, cpu_count,current_process,Manager,Value
from ctypes import c_char_p
import time

from tkinter import * # GUI
root=Tk()

display=lcd() # Lcd 16x2 I2c
lock =Lock()

# Adafruit PN532 RFID/NFC
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=False)

APROXIMA_CARTAO=("A P R O X I M E"," O C A R T A O")

class Application:

    def __init__(self):

        self.window=root
        self.config_window()
        self.update_clock()
        self.window.bind('<Key>', self.callback)
        root.mainloop()

    def config_window(self):

        self.window.title(u'Leitor de cartão magnético')
        self.window.attributes('-zoomed', True)
        photo = PhotoImage(file="images/lobo.png")
        self.window.iconphoto(False, photo)
        self.window["background"]="#0C3E69"
        self.window.maxsize(800,480)

        self.read_card=Button(self.window,text='Finalizar process',
                              background="#21629A", foreground="#CAE6FF",
                              border="11",font="Verdana 15 bold", #//Fonte, tamanho, tipo
                              width=40, height=5,
                              relief="groove", #Efeito { solid,sunken, etc.. ou nada }
                              command=lambda : self.finishing_process())

        self.read_cards=Button(self.window,text='Iniciar processo',
                              background="#21629A", foreground="#CAE6FF", border="11",
                              font="Verdana 15 bold", #//Fonte, tamanho, tipo
                              width=40, height=5,
                              relief="groove", #Efeito { solid,sunken, etc.. ou nada }
                              command=lambda :  self.new_process())

        self.press_exit=Button(self.window,text='Pressione para sair',
                              background="#21629A", foreground="#CAE6FF", border="11",
                              font="Verdana 15 bold", #//Fonte, tamanho, tipo
                              width=40, height=5,
                              relief="groove", #Efeito { solid,sunken, etc.. ou nada }
                              command=self.close_exit)

        self.read_card.pack()
        self.read_cards.pack()
        self.press_exit.pack()

        self.manager = Manager()
        self.maintenance = self.manager.Value(c_char_p, True)
        self.status_display = self.manager.Value(c_char_p, (None,None))

        self.thread_database_external = Process(target=self.sync_database_external)
        self.thread_database_external.start()

        self.thread_read_nfc = Process(target=self.read_nfc)
        self.thread_read_nfc.start()

        self.show_display()

    def close_exit(self):

        if self.thread_database_external:   self.thread_database_external.terminate()
        if self.thread_read_nfc:    self.thread_read_nfc.terminate()
        display.lcd_clear()
        self.window.destroy()

    def update_clock(self):

        print(current_process().name)
        print(cpu_count())
        print(self.thread_database_external.name , self.thread_database_external.is_alive())
        print(self.thread_read_nfc.name , self.thread_read_nfc.is_alive())

        now = datetime.now().strftime(" %d/%m/%Y %T")
        self.window.after(1000, self.update_clock)

    def callback(self, event):

        #--// Detecta tecla pŕessionada se for q/Q  fecha os processos e mata a interface
        if event.char in ['q','Q']: self.close_exit()

    def show_display(self):

        time.sleep(0.5)
        display.lcd_clear()

        line_1, line_2 = self.status_display.value
        display.lcd_display_string(line_1 if line_1 else APROXIMA_CARTAO[0], 1)
        display.lcd_display_string(line_2 if line_1 else APROXIMA_CARTAO[1], 2)

    def sync_database_external(self):

        while True:

            print("Entramos", self.maintenance.value)
            saida = getoutput("ping -c 1 10.0.0.102|grep rtt |awk '{print $4}'|cut -d'/' -f2|cut -d'.' -f1")
            if saida and int(saida) <=40:
                with lock:
                    print("Saida: ",saida )#,self.thread_database_external,self.thread_read_nfc.is_alive())

                try:
                    self.maintenance.value = False
                    self.status_display.value=("EM MANUTENCAO", "A G U A R D E")
                    self.show_display()

                    with lock:
                        print("Entrando na manutencao")
                    time.sleep(1)

                    with lock:
                        print("Saido da manutencao")
                    self.maintenance.value = True

                    self.status_display.value = (None, None)
                    self.show_display()
                    time.sleep(5)

                except:

                    with lock:
                        print("Pro blemas")
            else:
                with lock:
                    print("Rede fora de alcance")

    def read_nfc(self):

        while True:
            try:
                if self.maintenance.value:

                    pn532.SAM_configuration() # Configure PN532 to communicate with MiFare cards
                    uid = pn532.read_passive_target(timeout=0.5)
                    if uid:
                        self.status_display.value=("Seja bem vindo","Funcionario")
                        self.show_display()
                        time.sleep(0.5)

                        self.status_display.value = (None,None)
                        self.show_display()

            except:
                with lock:

                    time.sleep(0.5)
                    print("Erro na leitura")

if __name__ == '__main__':
    Application()