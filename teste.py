from tkinter import *
root = Tk()

w,h =  ( root.winfo_screenwidth() / 2) , ( root.winfo_screenheight() / 2 )
cor_fundo='#0C3E69'
root['bg']=cor_fundo
root.title("Testando Tkinter")

root.geometry("800x480")
#root.geometry("800x480+200+200")
#root.geometry("800x480+%d+%d" %(w,h))
w1, h1 = 800, 480
root.resizable(False,False)
root.minsize(width=w1,height=h1)
root.maxsize(width=w1,height=h1)


def lobo():
    print("Ola amigos...",w,h)

#---------[ LABEL ]
mensagem = Label(root,text="Coletor de dados  { lyk II }",bg=cor_fundo,fg='#ECECAC',font="Arial 20",width=w1/2, relief='flat', anchor=CENTER)
data_hora= Label(root,text="Horario: ",bg=cor_fundo,fg='#466F99',font="Arial 15",width=w1/2, relief='flat', anchor=E)
mensagem.pack()
data_hora.pack()

#anchor=CENTER | W | S | E { Alinhamento do TEXTO ]


#---------[  BOTAO ]
botao_1 = Button(root,text="Aproxime o cartao do leitor\nComo calma",font='Arial 30',width=w1, height=2,anchor=W,justify=LEFT,command=lobo)
botao_1.pack()

#botao_1.pack(side=LEFT)



root.mainloop()
