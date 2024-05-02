import tkinter as tk
from tkinter import filedialog, Label, messagebox
from AnalizadorLexico import analizador_lexico, generar_tabla_tokens_html, generar_tabla_errores_html
import codecs
from Instrucciones.Traductor import traducir_a_mongodb
from AnalizadorSintactico import *

class ScrollText(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.text = tk.Text(self, bg="#212121", foreground="#ffffff", insertbackground="#eeeeee", selectbackground="#757575", width=75, height=26, font=("Courier", 11),)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)
        self.numberLines = TextLineNumbers(self, width=35, bg="#444546")
        self.numberLines.attach(self.text)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.numberLines.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.text.bind("<Key>", self.onPressDelay)
        self.text.bind("<Button-1>", self.numberLines.redraw)
        self.scrollbar.bind("<Button-1>", self.onScrollPress)
        self.text.bind("<MouseWheel>", self.onPressDelay)

    def onScrollPress(self, *args):
        self.scrollbar.bind("<B1-Motion>", self.numberLines.redraw)

    def onPressDelay(self, *args):
        self.after(2, self.numberLines.redraw)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def redraw(self):
        self.numberLines.redraw()

    def delete(self, *args, **kwargs):
        self.text.delete(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        self.delete("all")
        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(
                2,
                y,
                anchor="nw",
                text=linenum,
                fill="#e8e8e8",
                font=("Courier New", 11, "bold"),
            )
            i = self.textwidget.index("%s+1line" % i)

class Ventana(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Proyecto 1")
        self.geometry("1500x510")
        self.config(background="#f0f0f0")
        self.resizable(0, 0)
        self.lbl_editable1 = Label(self, text="Texto De Entrada", bg=("#f0f0f0"), fg=("#151718"), font=("Times New Roman", 11))
        self.lbl_editable1.place(x=300, y=4)
        self.lbl_editable2 = Label(self, text="Texto De Salida", bg=("#f0f0f0"), fg=("#151718"), font=("Times New Roman", 11))
        self.lbl_editable2.place(x=1050, y=4)

        self.frame1 = ScrollText(self)
        self.frame1.place(x=5, y=25)

        self.frame2 = ScrollText(self)
        self.frame2.place(x=750, y=25)

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.ca = None
        self.filemenu1 = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Archivo", menu=self.filemenu1, background="#2b2b2b", foreground="white", activeforeground="black", activebackground="gray52")
        self.filemenu1.add_command(label="Nuevo", command=self.nuevo, background="#2b2b2b", foreground="white", activeforeground="black", activebackground="gray52")
        self.filemenu1.add_command(label="Abrir", command=self.abrir, background="#2b2b2b", foreground="white", activeforeground="black", activebackground="gray52")
        self.filemenu1.add_command(label="Guardar", command=self.guardar, background="#2b2b2b", foreground="white", activeforeground="black", activebackground="gray52")
        self.filemenu1.add_command(label="Guardar Como", command=self.guardarComo, background="#2b2b2b", foreground="white", activeforeground="black", activebackground="gray52")
        self.filemenu1.add_command(label="Salir", command=self.salir, background="#2b2b2b", foreground="white", activeforeground="black", activebackground="gray52")

        self.filemenu2 = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Análisis", menu=self.filemenu2, background="#2b2b2b", foreground="white", activeforeground="black", activebackground="gray52")
        self.filemenu2.add_command(label="Análisis",command=self.analisis, background="#2b2b2b", foreground="white", activeforeground="black", activebackground="gray52")

        self.filemenu3 = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Tokens", menu=self.filemenu3, background="#2b2b2b", foreground="white", activeforeground="black", activebackground="gray52")
        self.filemenu3.add_command(label="Tokens",command=self.tokens, background="#2b2b2b", foreground="white", activeforeground="black", activebackground="gray52")

        self.filemenu4 = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Errores", menu=self.filemenu4, background="#2b2b2b", foreground="white", activeforeground="black", activebackground="gray52")
        self.filemenu4.add_command(label="Errores",command=self.errores, background="#2b2b2b", foreground="white", activeforeground="black", activebackground="gray52")

    def nuevo(self):
        if self.frame1.get(1.0, tk.END) != "\n":
            if messagebox.askyesno("Guardar", "¿Desea guardar el archivo antes de cerrarlo?"):
                file_path = filedialog.asksaveasfilename(defaultextension=".lfp", filetypes=[("lfp files", "*.lfp")])
                if file_path:
                    with open(file_path, "w") as file:
                        file.write(self.frame1.get(1.0, tk.END))
        self.frame1.delete(1.0, tk.END)

    def abrir(self):
        file_path = filedialog.askopenfilename(filetypes=[("lfp files", "*.lfp")])
        if file_path:
            with codecs.open(file_path, "r", encoding='utf-8') as file:
                content = file.read()
                self.frame1.delete(1.0, tk.END)
                self.frame1.insert(tk.END, content)
            self.current_file = file_path

    def guardar(self):
        if self.current_file:  
            with open(self.current_file, "w", encoding='utf-8') as file:
                file.write(self.frame1.get(1.0, tk.END))
        else:
            file_path = filedialog.asksaveasfilename(defaultextension=".lfp", filetypes=[("lfp files", "*.lfp")])
            if file_path:
                with open(file_path, "w", encoding='utf-8') as file:
                    file.write(self.frame1.get(1.0, tk.END))
                self.current_file = file_path 

    def guardarComo(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".lfp", filetypes=[("lfp files", "*.lfp")])
        if file_path:
            with open(file_path, "w", encoding='utf-8') as file:
                file.write(self.frame1.get(1.0, tk.END))
            self.current_file = file_path

    def salir(self):
        Ventana.destroy(self)

    def analisis(self):
        # Obtener el texto del widget frame1
        texto = self.frame1.get(1.0, tk.END)
        
        # Traducir el texto utilizando la función traducir_a_mongodb
        texto_traducido = traducir_a_mongodb(texto)
        
        # Borrar el contenido actual del widget frame2
        self.frame2.delete(1.0, tk.END)
        
        # Insertar el texto traducido en el widget frame2
        self.frame2.insert(tk.END, texto_traducido)
        
        # Imprimir el texto traducido en la consola
        print(texto_traducido)


    def tokens(self):
        text = self.frame1.get(1.0, tk.END)
        lista_lexemas, lista_errores = analizador_lexico(text)
        generar_tabla_tokens_html(lista_lexemas)
        self.frame2.delete(1.0, tk.END)

    def errores(self):
        text = self.frame1.get(1.0, tk.END)
        lista_lexemas, lista_errores = analizador_lexico(text)
        generar_tabla_errores_html(lista_errores)
        self.frame2.delete(1.0, tk.END)

app = Ventana()
app.mainloop()
