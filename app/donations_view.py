from tkinter import LabelFrame,IntVar,CENTER,RIGHT,Y,NO,W,END,StringVar,Spinbox,Toplevel
from tkinter.ttk import Label,Entry, Button, Combobox,Checkbutton,Notebook,Frame,Treeview,Scrollbar
from ttkbootstrap import Style
from pandas import read_csv,DataFrame
from datetime import date


class DonationsView(Toplevel):
    def __init__(self):
        super().__init__()

        self.title('Solidarize')
        self.geometry('690x500')
        self.resizable(False,False)
        
        font = (None,12)

        label1 = Label(self,text='Recebidos',font=font)
        label1.grid(row=0,column=0,padx=10,pady=10)

        label2 = Label(self,text='Doados',font=font)
        label2.grid(row=0,column=1,padx=10,pady=10)
        
        columns = ('Subcategoria','Quantidade')
        
        self.my_tree1 = Treeview(self, show='headings',columns=columns,height=20)
        self.my_tree1.grid(row=1,column=0,padx=10,pady=10)
        
        for column in columns:
            self.my_tree1.heading(column,text=column,anchor=CENTER)
            self.my_tree1.column(column, anchor=CENTER, width=160)

        self.my_tree2 = Treeview(self, show='headings',columns=columns,height=20)
        self.my_tree2.grid(row=1,column=1,padx=10,pady=10)

        for column in columns:
            self.my_tree2.heading(column,text=column,anchor=CENTER)
            self.my_tree2.column(column, anchor=CENTER, width=160)


        self.load_data()
        



    def load_data(self):
        try:
            self.df1 = read_csv('./data-donations.csv')
        except:
            self.df1 = DataFrame({'data':[],'categoria':[],'subcategoria':[],'quantidade':[],'perecivel':[],'fragil':[]})

        try:
            self.df2 = read_csv('./data-transactions.csv')
        except:
            self.df2 = DataFrame({'data':[],'categoria':[],'subcategoria':[],'quantidade':[],'destino':[]})
             

        index1 = self.df1.groupby('subcategoria')['quantidade'].sum().index
        values1 = self.df1.groupby('subcategoria')['quantidade'].sum().values

        df1=DataFrame({'Subcategoria':index1,'Quantidade':values1})
        
        for index in df1.index:
           self.my_tree1.insert(parent='',index='end',iid=index,values=df1.loc[index].to_list())
        
        index2 = self.df2.groupby('subcategoria')['quantidade'].sum().index
        values2 = self.df2.groupby('subcategoria')['quantidade'].sum().values

        df2 = DataFrame({'Subcategoria':index2,'Quantidade':values2})
        
        for index in df2.index:
           self.my_tree2.insert(parent='',index='end',iid=index,values=df2.loc[index].to_list())
