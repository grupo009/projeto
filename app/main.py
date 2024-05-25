from tkinter import Toplevel,LabelFrame
from tkinter.ttk import Label,Button
from ttkbootstrap import Style
from received import Received,ReceivedInfo
from families import Families,FamiliesInfo
from donations import Donations
from donations_view import DonationsView

from pandas import read_csv

def received():
    global received_window
    try:
        received_window.destroy()
        received_window = Received()
    except:
        received_window = Received() 

def received_info():
    global received_info_window
    try:
        received_info_window.destroy()
        received_info_window = ReceivedInfo()
    except:
        received_info_window = ReceivedInfo()

def families():
    global families_window
    try:
        families_window.destroy()
        families_window = Families()
    except:
        families_window = Families()    

def families_info():
    global families_info_window
    try:
        families_info_window.destroy()
        families_info_window = FamiliesInfo()
    except:
        families_info_window = FamiliesInfo()



def donations():
    global donations_window
    try:
        donations_window.destroy()
        donations_window = Donations()
    except:
        donations_window = Donations()    

def donations_view():
    global donations_view_window
    try:
        donations_view_window.destroy()
        donations_view_window = DonationsView()
    except:
        donations_view_window = DonationsView()

style = Style(theme='cerculean')
main = style.master
main.title('Solidarize')
main.geometry('450x450')
main.resizable(False,False)



label1 = Label(main,text='Solidarize e Doe Certo!',font=('Harlow Solid Italic',25))
label1.pack(pady=20)

label2 = Label(main,text='Menu Principal',font=(None,12))
label2.pack(pady=10)



frame1 = LabelFrame(main,text='Recebidos')
frame1.pack(padx=10,pady=10)

btn1 = Button(frame1,text='Cadastrar ou Visualizar',command=received)
btn1.grid(row=0,column=0,padx=10,pady=10)

btn2 = Button(frame1,text='Estatísticas',command=received_info)
btn2.grid(row=0,column=1,padx=10,pady=10)



frame2 = LabelFrame(main,text='Famílias')
frame2.pack(padx=10,pady=10)

btn3 = Button(frame2,text='Cadastrar ou Visualizar',command=families)
btn3.grid(row=0,column=0,padx=10,pady=10)

btn4 = Button(frame2,text='Estatísticas',command=families_info)
btn4.grid(row=0,column=1,padx=10,pady=10)



frame3 = LabelFrame(main,text='Doações')
frame3.pack(padx=10,pady=10)

btn5 = Button(frame3,text='Registrar',command=donations)
btn5.grid(row=0,column=0,padx=10,pady=10)

btn6 = Button(frame3,text='Visualizar',command=donations_view)
btn6.grid(row=0,column=1,padx=10,pady=10)


main.mainloop()
