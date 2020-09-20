#!/usr/sbin/evn python3
# Jose de Almeida Lobino 2020-09-19

# Module Adafruit PN532 RFID/NFC
import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI

# Module Lcd 16x2 I2c
from libs.lcddriver import lcd

from tkinter import * # GUI
from datetime import datetime
from threading import Thread
from subprocess import getoutput
from multiprocessing import Process
import time

root=Tk()
display=lcd() # Lcd 16x2 I2c

# Adafruit PN532 RFID/NFC
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=False)

class Application:

    def __init__(self):

        self.window=root
        self.config_window()


        #self.show_display()
        #x = Thread(target=self.thread_sync_database_external, args=(1,))
        #x.start()
        root.mainloop()

    def config_window(self):

        self.window.title(u'Leitor de cartão magnético')
        self.window.attributes('-zoomed', True)
        photo = PhotoImage(file="images/lobo.png")
        self.window.iconphoto(False, photo)
        self.window["background"]="#0C3E69"
        self.window.minsize(700,400)

        self.read_card=Button(self.window,text='Finalizar process',
                              background="#21629A",
                              foreground="#CAE6FF",
                              border="11",
                              font="Verdana 15 bold", #//Fonte, tamanho, tipo
                              width=40,
                              height=5,
                              relief="groove", #Efeito { solid,sunken, etc.. ou nada }
                              command=lambda : self.finishing_process())

        self.read_cards=Button(self.window,text='Iniciar processo',
                              background="#21629A",
                              foreground="#CAE6FF",
                              border="11",
                              font="Verdana 15 bold", #//Fonte, tamanho, tipo
                              width=40,
                              height=5,
                              relief="groove", #Efeito { solid,sunken, etc.. ou nada }
                              command=lambda :  self.new_process())

        self.press_exit=Button(self.window,text='Pressione para sair',
                              background="#21629A",
                              foreground="#CAE6FF",
                              border="11",
                              font="Verdana 15 bold", #//Fonte, tamanho, tipo
                              width=40,
                              height=5,
                              relief="groove", #Efeito { solid,sunken, etc.. ou nada }
                              command=self.exit_press)

        self.read_card.pack()
        self.read_cards.pack()
        self.press_exit.pack()

        #self.sql_maintenance = False

        #self.thread_read_nfc=None
        self.show_display()
        self.thread_database_external = Process(target=self.sync_database_external)
#        self.thread_read_nfc = Process(target=self.read_nfc)

        self.thread_database_external.start()
 #       self.thread_read_nfc.start()


    def new_process(self):
        self.sql_maintenance = False
        #if not self.thread_read_nfc.is_alive():

         #   del self.thread_read_nfc

          #  self.thread_read_nfc = Process(target=self.read_nfc)
          #  self.thread_read_nfc.start()

    def finishing_process(self):
        #print("Pedido de finalizacao")
        #if self.thread_read_nfc.is_alive():
         #   self.thread_read_nfc.terminate()
          #  print("Finalizado")
        self.sql_maintenance=False

    def sync_database_external(self):

        self.thread_read_nfc = Process(target=self.read_nfc)
        self.thread_read_nfc.start()

        while True:

            saida = getoutput("ping -c 1 10.0.0.102|grep rtt |awk '{print $4}'|cut -d'/' -f2|cut -d'.' -f1")
            if saida and int(saida) <=40:
                print("Saida: ",saida,self.thread_database_external)

                try:
                    if self.thread_read_nfc.is_alive():
                        self.thread_read_nfc.terminate()
                        self.show_display(args=("EM MANUTENCAO", "A G U A R D E"), maintenance=True)
                        print('*****************************************************************')

                        time.sleep(2)
                        self.sql_maintenance = True
                except: pass
            else:   print("Fora de alcance")

            try:
                if not self.thread_read_nfc.is_alive():
                    print("/////////////////////////////////////////////")
                    del self.thread_read_nfc

                    self.thread_read_nfc = Process(target=self.read_nfc)
                    self.thread_read_nfc.start()
                    self.show_display()
                    print('-----------------------------------------------------------------')
            except:
                self.show_display(args=("ACESSANDO", "AGUARDE..."), maintenance=True)


        self.thread_read_nfc = Process(target=self.read_nfc)
        self.thread_read_nfc.start()

    def exit_press(self):

        if self.thread_database_external:  self.thread_database_external.terminate()
        #if self.thread_read_nfc:    self.thread_read_nfc.terminate()
        display.lcd_clear()
        self.window.destroy()

    def show_display(self,args=(None,None), maintenance=False):

        line_1, line_2=args
        display.lcd_clear()
        if line_1:  display.lcd_display_string(line_1, 1)
        if line_2:  display.lcd_display_string(line_2, 2)

        if not maintenance:
            time.sleep(1)
            display.lcd_display_string("A P R O X I M E", 1)
            display.lcd_display_string(" O C A R T A O", 2)

    def read_nfc(self):

        while True:
            pn532.SAM_configuration() # Configure PN532 to communicate with MiFare cards
            uid = pn532.read_passive_target(timeout=0.5)
            if uid: self.show_display(args=('Seja bem vindo','Funcionario'))
if __name__ == '__main__':
    Application()

