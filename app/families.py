from tkinter import LabelFrame,IntVar,CENTER,RIGHT,Y,NO,W,END,StringVar,Spinbox,Toplevel,BOTTOM,X,HORIZONTAL
from tkinter.ttk import Label,Entry, Button, Combobox,Checkbutton,Notebook,Frame,Treeview,Scrollbar
from ttkbootstrap import Style
from pandas import read_csv,DataFrame
from datetime import date as dt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot
from matplotlib.ticker import PercentFormatter
import numpy

class Families(Toplevel):
    def __init__(self):
        super().__init__()
        
        self.geometry('1250x700')
        self.resizable(False,False)
        
        tree_frame = LabelFrame(self,text='Todos os Registros')
        tree_frame.pack(padx=20,pady=10)

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        tree_scroll2 = Scrollbar(tree_frame,orient=HORIZONTAL)
        tree_scroll2.pack(side=BOTTOM, fill=X)


        columns = ('rg','cpf','nis','cras','nome','data_nascimento','endereco','estado_civil','escolaridade','situacao','beneficio','familia','renda')
        self.my_tree = Treeview(tree_frame, show='headings',xscrollcommand=tree_scroll2.set,yscrollcommand=tree_scroll.set, selectmode="extended",columns=columns)
        self.my_tree.pack()

        tree_scroll.config(command=self.my_tree.yview)
        tree_scroll2.config(command=self.my_tree.xview)

        for column in columns:
            self.my_tree.heading(column, text=column, anchor=CENTER)
            self.my_tree.column(column, anchor=CENTER, width=150)

        self.load_data()


        data_frame = LabelFrame(self,text='Dados do Registro')
        data_frame.pack(fill='x',expand='yes',padx=20)
        
        self.nome = StringVar()
        self.rg = StringVar()
        self.cpf = StringVar()
        self.nis = StringVar()
        self.cras = StringVar()
        self.nascimento = StringVar()
        self.adress = StringVar()
        self.estado_civil = StringVar()
        self.escolaridade = StringVar()
        self.emprego = StringVar()
        self.beneficio = StringVar()
        self.familia = IntVar()
        self.renda_total = StringVar()
        self.renda_per_capta = StringVar()
        
        self.clear()

        label1 = Label(data_frame,text='Nome')
        label1.grid(row=0,column=0,padx=10,pady=10)

        entry1 = Entry(data_frame,textvariable=self.nome)
        entry1.grid(row=0,column=1,pady=10)

        label2 = Label(data_frame,text='RG')
        label2.grid(row=0,column=2,padx=10,pady=10)

        self.entry2 = Entry(data_frame,textvariable=self.rg)
        self.entry2.grid(row=0,column=3,padx=10,pady=10)
        self.entry2.bind('<KeyRelease>',self.format_rg)

        label3 = Label(data_frame,text='CPF')
        label3.grid(row=0,column=4,padx=10,pady=10)
        
        self.entry3 = Entry(data_frame,textvariable=self.cpf)
        self.entry3.grid(row=0,column=5,padx=10,pady=10)
        self.entry3.bind('<KeyRelease>', self.format_cpf)

        label4 = Label(data_frame,text='NIS')
        label4.grid(row=1,column=0,padx=10,pady=10)

        entry4 = Entry(data_frame,textvariable=self.nis)
        entry4.grid(row=1,column=1)

        check1 = Checkbutton(data_frame,text='Possuí Cadastro CRAS?',variable=self.cras,onvalue='Sim',offvalue='Não')
        check1.grid(row=1,column=2,padx=10,pady=10,columnspan=2)

        combo1 = Combobox(data_frame,textvariable=self.emprego,
                            values=['Desempregado','Trabalho Formal','Autônomo','Trabalho Informal'],
                            state='readonly')
        combo1.grid(row=1,column=4,padx=10,pady=10)
        
        combo2 = Combobox(data_frame,textvariable=self.beneficio,
                            values=['Nenhum','Bolsa Família','Auxílio Brasil','PBC/LOAS','Pensão por Morte','Aposentadoria','Outros/Vários'],
                            state='readonly')
        combo2.grid(row=1,column=5,padx=10,pady=10)

        label5= Label(data_frame,text='Data de Nascimento')
        label5.grid(row=2,column=0,padx=10,pady=10)

        self.entry5 = Entry(data_frame,textvariable=self.nascimento)
        self.entry5.grid(row=2,column=1,padx=10,pady=10)
        self.entry5.bind('<KeyRelease>',self.format_nascimento)

        combo3 = Combobox(data_frame,textvariable=self.escolaridade,
            values=['Fundamental Incompleto',
                    'Fundamental Completo',
                    'Médio Incompleto',
                    'Médio Completo'
                    ],
            state='readonly'
            )
        combo3.grid(row=2,column=2,padx=10,pady=10)


        combo4 = Combobox(data_frame,textvariable=self.estado_civil,
                        values=['Solteiro(a)','Casado(a)','Viúvo(a)'],
                        state='readonly'
                        )
        combo4.grid(row=2,column=5,padx=10,pady=10)

        label6 = Label(data_frame,text='Número de pessoas')
        label6.grid(row=3,column=0,padx=10,pady=10)

        entry6 = Entry(data_frame,textvariable=self.familia)
        entry6.grid(row=3,column=1,padx=10,pady=10)

        label7 = Label(data_frame,text='Renda Familiar (R$)')
        label7.grid(row=3,column=2,padx=10,pady=10)

        self.entry7 = Entry(data_frame,textvariable=self.renda_total)
        self.entry7.grid(row=3,column=3,padx=10,pady=10)
        self.entry7.bind('<KeyRelease>',self.calcula_renda)

        label8 = Label(data_frame,text='Renda per Capta (R$)')
        label8.grid(row=3,column=4,padx=10,pady=10)

        entry8 = Entry(data_frame,textvariable=self.renda_per_capta,state='readonly')
        entry8.grid(row=3,column=5,padx=10,pady=10)

        label9 = Label(data_frame,text='Endereço')
        label9.grid(row=4,column=0,padx=10,pady=10)

        entry9 = Entry(data_frame,width=100,textvariable=self.adress)
        entry9.grid(row=4,column=1,columnspan=5,pady=10)
        
        options_frame = LabelFrame(self,text='Opções')
        options_frame.pack(fill='x',expand='yes',padx=20)

        limpar = Button(options_frame,text='Limpar',command=self.clear)
        limpar.grid(row=0,column=0,padx=10,pady=10)

        registrar=Button(options_frame,text='Salvar Novo Registro',command=self.save_new)
        registrar.grid(row=0,column=1,padx=10,pady=10)

        alterar = Button(options_frame,text='Salvar Alteração',command=self.save_changes)
        alterar.grid(row=0,column=2,padx=10,pady=10)

        label10 = Label(options_frame)
        label10.grid(row=0,column=3,padx=50,pady=10)

        pesquisar = Button(options_frame,text='Pesquisar',command=self.search)
        pesquisar.grid(row=0,column=4,padx=10,pady=10)

        self.combo4 = Combobox(options_frame,values=['nome','rg','cpf'],state='readonly')
        self.combo4.set('nome')
        self.combo4.grid(row=0,column=5,padx=10,pady=10)

        


        self.my_tree.bind('<ButtonRelease-1>',self.select_record)

    selected_index = 0

    def format_rg(self,event=None):
        text = self.entry2.get().replace(".", "").replace("-", "")[:10]

        new_text = ''

        if event.keysym.lower() == 'backspace': return

        for index in range(len(text)):
            if not text[index] in "0123456789": continue
            if index in [1,4]: 
                new_text += text[index] + "."
            elif index == 7: 
                new_text += text[index] + "-"
            else: 
                new_text += text[index]

        self.entry2.delete(0, "end")
        self.entry2.insert(0, new_text)


    
    def format_cpf(self,event = None):
        text = self.entry3.get().replace(".", "").replace("-", "")[:11]
        
        new_text = ''

        if event.keysym.lower() == 'backspace': return

        for index in range(len(text)):
            if not text[index] in "0123456789": continue
            if index in [2, 5]: 
                new_text += text[index] + "."
            elif index == 8: 
                new_text += text[index] + "-"
            else: 
                new_text += text[index]

        self.entry3.delete(0, "end")
        self.entry3.insert(0, new_text)

    def format_nascimento(self,event=None):
        text = self.entry5.get().replace("/", "")[:8]

        new_text = ''

        if event.keysym.lower() == 'backspace': return

        for index in range(len(text)):
            if not text[index] in "0123456789": continue
            if index in [1, 3]: 
                new_text += text[index] + "/"
            else:
                new_text += text[index]

        self.entry5.delete(0, "end")
        self.entry5.insert(0, new_text)



    def calcula_renda(self,event):
        text = self.entry7.get().replace(",", "")[:8]
        new_text = ''

        if event.keysym.lower() == 'backspace': return

        for index in range(len(text)):
            cont=len(text)
            if not text[index] in "0123456789": continue
            if index in [cont-3]: new_text += text[index] + ","
            else: new_text += text[index]
        
        try:
            value = float(new_text.replace(',','.'))
            family_size = int(self.familia.get())
        except:
            value = 0
            family_size =1
            self.familia.set(1)

        self.entry7.delete(0,'end')
        self.entry7.insert(0,new_text)
        
        self.renda_per_capta.set(str(round(value/family_size,2)))
        

    def load_data(self):
        try:
            self.df=read_csv('./data-families.csv').astype('str')
            for index in self.df.index:
                self.my_tree.insert(parent='',index='end',iid=index,values=self.df.loc[index].to_list())
        except:
            self.df = DataFrame({'rg':[],'cpf':[],'nis':[],'cras':[],
            'nome':[],'data_nascimento':[],'endereco':[],'estado_civil':[],
            'escolaridade':[],'situacao':[],'beneficio':[],'familia':[],'renda':[]})

    def select_record(self,event):
        selected = self.my_tree.focus()
        values = self.my_tree.item(selected,'values')
        if type(values) != str:
            self.nome.set(values[4])
            self.rg.set(values[0])
            self.cpf.set(values[1])
            self.nis.set(values[2])
            self.cras.set(values[3])
            self.nascimento.set(values[5])
            self.adress.set(values[6])
            self.estado_civil.set(values[7])
            self.escolaridade.set(values[8])
            self.emprego.set(values[9])
            self.beneficio.set(values[10])
            self.familia.set(values[11])
            self.renda_total.set(str(float(values[12].replace(',','.'))*float(values[11])))
            self.renda_per_capta.set(values[12])

            self.selected_index=int(selected)

    def clear(self):
        self.nome.set('')
        self.rg.set('')
        self.cpf.set('')
        self.nis.set('')
        self.cras.set('Não')
        self.nascimento.set('')
        self.adress.set('')
        self.estado_civil.set('Estado Civil')
        self.escolaridade.set('Escolaridade')
        self.emprego.set('Situação de Trabalho')
        self.beneficio.set('Benefício')
        self.familia.set(1)
        self.renda_total.set('')
        self.renda_per_capta.set('0,00')

    def save_new(self):
        values = {}
        values['nome'] = self.nome.get()
        values['rg'] = self.rg.get()
        values['cpf'] = self.cpf.get()
        values['nis'] = self.nis.get()
        values['cras'] = self.cras.get()
        values['data_nascimento'] = self.nascimento.get()
        values['endereco'] = self.adress.get()
        values['estado_civil'] = self.estado_civil.get()
        values['escolaridade'] = self.escolaridade.get()
        values['situacao'] = self.emprego.get()
        values['beneficio'] = self.beneficio.get()
        values['familia'] = self.familia.get()
        values['renda'] = self.renda_per_capta.get()
        
        if not '' in values.values():
            if not (values['estado_civil'] == 'Estado Civil' or 
                    values['escolaridade'] == 'Escolaridade' or 
                    values['situacao'] == 'Situação de Trabalho' or
                    values['beneficio']=='Beneficio'):

                for index in self.df.index:
                    self.my_tree.delete(index)

                self.df.loc[len(self.df)] = values
                self.df.to_csv('./data-families.csv',index=False)

                self.load_data()
                self.clear()

 

    def save_changes(self):
        values = {}
        values['nome'] = self.nome.get()
        values['rg'] = self.rg.get()
        values['cpf'] = self.cpf.get()
        values['nis'] = self.nis.get()
        values['cras'] = self.cras.get()
        values['data_nascimento'] = self.nascimento.get()
        values['endereco'] = self.adress.get()
        values['estado_civil'] = self.estado_civil.get()
        values['escolaridade'] = self.escolaridade.get()
        values['situacao'] = self.emprego.get()
        values['beneficio'] = self.beneficio.get()
        values['familia'] = self.familia.get()
        values['renda'] = self.renda_per_capta.get()

        if not '' in values.values():
            if not (values['estado_civil'] == 'Estado Civil' or
                    values['escolaridade'] == 'Escolaridade' or
                    values['situacao'] == 'Situação de Trabalho' or
                    values['beneficio']=='Beneficio'):

                for index in self.df.index:
                    self.my_tree.delete(index)
        
                self.df.loc[self.selected_index] = values
                self.df.to_csv('./data-families.csv',index=False)

                self.load_data()
                self.clear()



    def search(self):
        search_variable = self.nome.get()
        option = self.combo4.get()
        
        try:
            if option == 'nome':
                search_variable = self.nome.get()
            elif option == 'rg':
                search_variable = self.rg.get()
            else:
                search_variable = self.cpf.get()
            
            values = self.df.query(f'{option} == "{search_variable}"').iloc[0,:].values
                
            self.rg.set(values[0])
            self.cpf.set(values[1])
            self.nis.set(values[2])
            self.cras.set(values[3])
            self.nome.set(values[4])
            self.nascimento.set(values[5])
            self.adress.set(values[6])
            self.estado_civil.set(values[7])
            self.escolaridade.set(values[8])
            self.emprego.set(values[9])
            self.beneficio.set(values[10])
            self.familia.set(values[11])
            self.renda_total.set(str(float(values[12].replace(',','.'))*float(values[11])))
            self.renda_per_capta.set(values[12])
        except:
            pass        


class FamiliesInfo(Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Solidarize')
        #self.geometry('1100x500')
        self.resizable(False,False)

        df = read_csv('./data-families.csv')
        
        frame1 = LabelFrame(self)
        frame1.pack()

        dff = df['cras'].value_counts()
        colors = ['#4DC9E6','#48B2DF','#429AD8','#3D83D1','#376BCA']

        fig1, ax1 = pyplot.subplots()
        pyplot.title('Percentual de Pessoas que possuem CRAS')
        ax1.pie(dff.values/len(df),labels=dff.index,colors=colors,autopct='%1.2f%%')

        canvas1 = FigureCanvasTkAgg(fig1,frame1)
        canvas1.draw()
        canvas1.get_tk_widget().grid(row=0,column=0)

        
        dff = df['escolaridade'].value_counts()

        fig2, ax2 = pyplot.subplots()
        pyplot.title('Escolaridade')
        ax2.pie(dff.values/len(df),labels=dff.index,colors=colors,autopct='%1.2f%%')

        canvas2 = FigureCanvasTkAgg(fig2,frame1)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=0,column=1)

        dff = df['beneficio'].value_counts()

        fig3, ax3 = pyplot.subplots()
        pyplot.title('Percentual de Pessoas que recebem algum benefício')
        ax3.pie(dff.values/len(df),labels=dff.index,colors=colors,autopct='%1.2f%%')

        canvas3 = FigureCanvasTkAgg(fig3,frame1)
        canvas3.draw()
        canvas3.get_tk_widget().grid(row=1,column=0)

        dff = df['renda']
        
        fig4, ax4 = pyplot.subplots()
        pyplot.title('Renda Per Capta (R$)')
        ax4.hist(dff,weights=numpy.ones(len(df))/len(df))
        pyplot.gca().yaxis.set_major_formatter(PercentFormatter(1))
        pyplot.xlabel('Renda per Capta (R$))')

        canvas4 = FigureCanvasTkAgg(fig4,frame1)
        canvas4.draw()
        canvas4.get_tk_widget().grid(row=1,column=1)



