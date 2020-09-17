from tkinter import *
from libs.lcddriver import lcd
from datetime import datetime
import time

root=Tk()
display=lcd()

class Application:

    def __init__(self):

        self.window=root
        self.config_window()
        self.update_clock()
        root.mainloop()

    def config_window(self):

        self.window.title(u'Leitor de cartão magnético')
        self.window.attributes('-zoomed', True)
        photo = PhotoImage(file="images/lobo.png")
        self.window.iconphoto(False, photo)
        self.window["background"]="#0C3E69"
        self.window.minsize(700,400)

        self.read_card=Button(self.window,text='Simular leitura do cartão',
                              background="#21629A",
                              foreground="#CAE6FF",
                              border="11",
                              font="Verdana 15 bold", #//Fonte, tamanho, tipo
                              width=40,
                              height=5,
                              relief="groove", #Efeito { solid,sunken, etc.. ou nada }
                              command=self.employee)

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
        self.press_exit.pack()

    def exit_press(self):
        self.window.destroy()

    def employee(self):

        self.show_display(line_2='Ola Lobinho')
        time.sleep(1.5)

    def update_clock(self):
        self.show_display()
        self.window.after(1000, self.update_clock)

    def show_display(self,line_1=None, line_2=None):

        now=datetime.now().strftime(" %d/%m %H:%M:%S ")
        if not line_1:  line_1=now
        if not line_2:  line_2=" Passe o cartao "
        else:   display.lcd_display_string((" "*16), 2)

        display.lcd_display_string(line_1, 1) # Write line of text to first line of display
        if line_2:  display.lcd_display_string(line_2, 2) # Write line of text to second line of display

Application()