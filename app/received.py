from tkinter import LabelFrame,IntVar,CENTER,RIGHT,Y,NO,W,END,StringVar,Spinbox,Toplevel
from tkinter.ttk import Label,Entry, Button, Combobox,Checkbutton,Notebook,Frame,Treeview,Scrollbar
from pandas import read_csv,DataFrame,to_datetime
from datetime import date as dt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot


class Received(Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Solidarize')
        self.geometry('1100x500')
        self.resizable(False,False)
        
        self.df = DataFrame()

        tree_frame = LabelFrame(self,text='Todos os Registros')
        tree_frame.pack(pady=10,padx=10)
        
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)
        
        columns = ('data','categoria','subcategoria','quantidade','perecivel','fragil')
        
        self.my_tree = Treeview(tree_frame, show='headings',yscrollcommand=tree_scroll.set,columns=columns)
        self.my_tree.pack()
        
        tree_scroll.config(command=self.my_tree.yview)
        
        for column in columns:
            self.my_tree.heading(column,text=column,anchor=CENTER)
            self.my_tree.column(column, anchor=CENTER, width=150)
        
        self.load_data()

        data_frame = LabelFrame(self,text='Dados do Registro')
        data_frame.pack(fill='x',expand='yes',padx=20)

      
        self.categorias = {'Brinquedos':['Brinquedos de Bebê','Brinquedos de Criança'],
                    'Alimento':['Arroz','Feijão','Óleo','Cesta Básica','Hortifruti'],
                    'Eletrodomésticos':['Geladeira','Fogão','Televisão','Outros'],
                    'Eletrônicos':['Celular','Computador','Tablet'],
                    'Roupas':['Aviamentos e Acessórios','Roupa Masculina','Roupa Feminina','Roupa Infantil','Roupa de Bebê'],
                    'Móveis':['Cama','Sofá','Guarda-Roupa','Mesa'],
                    'Papelaria':['Artesanato','Material Escolar']}
        
        self.data_registro = StringVar()
        self.categoria = StringVar()
        self.subcategoria = StringVar()
        self.quantidade = IntVar()
        self.perishable = StringVar()
        self.fragile = StringVar()
        self.donated = StringVar()
        
        self.clear()

        self.combo1 = Combobox(data_frame,values=list(self.categorias.keys()),state='readonly',textvariable=self.categoria)
        self.combo1.grid(row=0,column=0,padx=10,pady=10)
        self.combo1.bind('<<ComboboxSelected>>',self.sub_choice)
        
        self.combo2 = Combobox(data_frame,values=[],state='readonly',textvariable=self.subcategoria)
        self.combo2.grid(row=0,column=1,padx=10,pady=10)

        label1 = Label(data_frame,text='Quantidade')
        label1.grid(row=0,column=3,padx=10,pady=10)

        spinbox1 = Spinbox(data_frame,width=10,from_=1,to=1000,textvariable=self.quantidade)
        spinbox1.grid(row=0,column=4,padx=10,pady=10)

        check1 = Checkbutton(data_frame,text='Perecível',onvalue='Sim',offvalue='Não',variable=self.perishable)
        check1.grid(row=0,column=5,padx=10,pady=10)

        check2 = Checkbutton(data_frame,text='Frágil',onvalue='Sim',offvalue='Não',variable=self.fragile)
        check2.grid(row=0,column=6,padx=10,pady=10)


        options_frame = LabelFrame(self,text='Opções')
        options_frame.pack(fill='x',expand='yes',padx=20)

        limpar = Button(options_frame,text='Limpar',command=self.clear)
        limpar.grid(row=0,column=0,padx=10,pady=10)

        registrar=Button(options_frame,text='Salvar Novo Registro',command=self.save_new)
        registrar.grid(row=0,column=1,padx=10,pady=10)

        alterar = Button(options_frame,text='Salvar Alteração',command=self.save_changes)
        alterar.grid(row=0,column=2,padx=10,pady=10)


        self.my_tree.bind('<ButtonRelease-1>',self.select_record)

    selected_index=0
    
    def sub_choice(self,event):
        
        self.combo2.config(values=self.categorias[self.categoria.get()])
        


    def load_data(self):
        try:
          
            self.df = read_csv('./data-donations.csv')
            self.df = self.df.sort_values(by='data',ascending=False)
            self.df = self.df.reset_index(drop=True)
            for index in self.df.index:
                self.my_tree.insert(parent='',index='end',iid=index,values=self.df.loc[index].to_list())
            
        except:
            self.df = DataFrame({'data':[],'categoria':[],'subcategoria':[],'quantidade':[],'perecivel':[],'fragil':[]})
    
    def select_record(self,event):
        selected = self.my_tree.focus()
        values = self.my_tree.item(selected, 'values')
        if type(values) != str:
            self.data_registro.set(values[0])
            self.categoria.set(values[1])
            self.subcategoria.set(values[2])
            self.quantidade.set(values[3])
            self.perishable.set(values[4])
            self.fragile.set(values[5])
            
            self.selected_index=selected


    def clear(self):
        self.data_registro.set(str(dt.today().strftime('%d/%m/%Y')))
        self.categoria.set('Categoria')
        self.subcategoria.set('Subcategoria')
        self.quantidade.set(1)
        self.perishable.set('Sim')
        self.fragile.set('Sim')


    def save_new(self):
        values={}
        values['data'] = str(dt.today())
        values['categoria'] = self.categoria.get()
        values['subcategoria']= self.subcategoria.get()
        values['quantidade']=int(self.quantidade.get())
        values['perecivel'] = self.perishable.get()
        values['fragil'] = self.fragile.get()
    
        try:
            for index in self.df.index:
                self.my_tree.delete(index)
        except:
            pass

        if (values['categoria']=='Categoria' or values['subcategoria']=='Subcategoria'):
            #print('dados inválidos')
            pass
        else:        
            self.df.loc[len(self.df)] = values
            self.df.to_csv('./data-donations.csv',index=False)
    
        self.load_data()

        self.clear()


    def save_changes(self):
        values={}
        values['data']=self.data_registro.get()
        values['categoria'] = self.categoria.get()
        values['subcategoria']= self.subcategoria.get()
        values['quantidade']=int(self.quantidade.get())
        values['perecivel'] = self.perishable.get()
        values['fragil'] = self.fragile.get()

        self.df.loc[int(self.selected_index)] = values
        
        self.df.to_csv('./data-donations.csv',index=False)
        
        for index in self.df.index:
            self.my_tree.delete(index)
    
        self.load_data()
    
        self.clear()




class ReceivedInfo(Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Solidarize')
        #self.geometry('1500x500')
        self.resizable(False,False)

        df = read_csv('data-donations.csv')
        df['data'] = df['data'].astype('datetime64[ns]')
        df = df.set_index(df['data'])

        frame1 = LabelFrame(self)
        frame1.pack()

        dff = df['categoria'].value_counts()
        colors = ['#4DC9E6','#48B2DF','#429AD8','#3D83D1','#376BCA']

        fig1, ax1 = pyplot.subplots()
        pyplot.title('Categoria das Doações')
        ax1.pie(dff.values/len(df),labels=dff.index,colors=colors,autopct='%1.2f%%')

        canvas1 = FigureCanvasTkAgg(fig1,frame1)
        canvas1.draw()
        canvas1.get_tk_widget().grid(row=0,column=0)

        dff = df.index.month.value_counts()

        fig2,ax2 = pyplot.subplots()
        pyplot.title('Doações Mensais')
        ax2.bar(dff.index,dff.values,color='#429AD8')
        pyplot.xticks([x for x in range(1,13)])

        canvas2 = FigureCanvasTkAgg(fig2,frame1)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=0,column=1)

