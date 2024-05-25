from tkinter import LabelFrame,IntVar,CENTER,RIGHT,Y,NO,W,END,StringVar,Spinbox,Toplevel
from tkinter.ttk import Label,Entry, Button, Combobox,Checkbutton,Notebook,Frame,Treeview,Scrollbar
from pandas import read_csv,DataFrame,to_datetime
from datetime import date as dt


class Donations(Toplevel):
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
        
        columns = ('data','categoria','subcategoria','quantidade','documento')
        
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
        self.documento = StringVar()
        
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
        
        label2 = Label(data_frame,text='RG')
        label2.grid(row=0,column=5,padx=10,pady=10)

        entry1 = Entry(data_frame,textvariable=self.documento)
        entry1.grid(row=0,column=6,padx=10,pady=10)

        options_frame = LabelFrame(self,text='Opções')
        options_frame.pack(fill='x',expand='yes',padx=20)

        limpar = Button(options_frame,text='Limpar',command=self.clear)
        limpar.grid(row=0,column=0,padx=10,pady=10)

        registrar = Button(options_frame,text='Registrar Doação',command=self.save_new)
        registrar.grid(row=0,column=2,padx=10,pady=10)

        alterar = Button(options_frame,text='Salvar Alteração',command=self.save_changes)
        alterar.grid(row=0,column=3,padx=10,pady=10)

        self.my_tree.bind('<ButtonRelease-1>',self.select_record)

    selected_index=0
    
    def sub_choice(self,event):
       self.combo2.config(values=self.categorias[self.categoria.get()])
        

    def load_data(self):
        try:
            self.df = read_csv('./data-transactions.csv')
            self.df = self.df.sort_values(by='data',ascending=False)
            self.df = self.df.reset_index(drop=True)
            self.df['documento'] = self.df['documento'].astype('string')
            
            for index in self.df.index:
                self.my_tree.insert(parent='',index='end',iid=index,values=self.df.loc[index].to_list())
            
        except:
            self.df = DataFrame({'data':[],'categoria':[],'subcategoria':[],'quantidade':[],'documento':[]})

    def select_record(self,event):
        selected = self.my_tree.focus()
        values = self.my_tree.item(selected, 'values')
        if type(values) != str:
            self.data_registro.set(values[0])
            self.categoria.set(values[1])
            self.subcategoria.set(values[2])
            self.quantidade.set(values[3])
            self.documento.set(values[4])
            
            self.selected_index=int(selected)


    def clear(self):
        self.data_registro.set(str(dt.today()))
        self.categoria.set('Categoria')
        self.subcategoria.set('Subcategoria')
        self.quantidade.set(1)
        self.documento.set('')

    def add_itens(self):
        ...


    def save_new(self):
        values={}
        values['data'] = str(dt.today())
        values['categoria'] = self.categoria.get()
        values['subcategoria']= self.subcategoria.get()
        values['quantidade']=self.quantidade.get()
        values['documento'] = str(self.documento.get())

        if not (values['categoria'] == 'Categoria' or
                values['subcategoria'] == 'Subcategoria' or
                values['documento'] == ''):

            try:
                for index in self.df.index:
                    self.my_tree.delete(index)
            except:
                pass
        
            self.df.loc[len(self.df)] = values

            self.df.to_csv('./data-transactions.csv',index=False)
    
            self.load_data()
        
            self.clear()


    def save_changes(self):
        values={}
        values['data']=self.data_registro.get()
        values['categoria'] = self.categoria.get()
        values['subcategoria']= self.subcategoria.get()
        values['quantidade']=self.quantidade.get()
        values['documento']=str(self.documento.get())

        if not (values['categoria'] == 'Categoria' or
                values['subcategoria'] == 'Subcategoria' or
                values['documento'] == ''):

            try:
                self.df.loc[int(self.selected_index)] = values
        
                self.df.to_csv('./data-transactions.csv',index=False)
        
                for index in self.df.index:
                    self.my_tree.delete(index)
        
                self.load_data()
    
                self.clear()
            except:
                ...


