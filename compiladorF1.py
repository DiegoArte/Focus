import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
from PIL import Image,ImageTk
from tkinter import messagebox
import re
import time
import difflib


def abrir_archivo():
    file_path = filedialog.askopenfilename()
    global rutaFile
    rutaFile = file_path
    if file_path:
        with open(file_path, 'r') as file:
            text = file.read()
            cajaCodigo.delete('1.0', tk.END)
            cajaCodigo.insert(tk.END, text)
            colorear_palabras()
            
def guardar_archivo():
    #print("Ruta: ",rutaFile)
    codigo = cajaCodigo.get("1.0", tk.END)
    #Si no se abrió un archivo y se comenzó a codificar
    if rutaFile == "":
        # Abrir un cuadro de diálogo para seleccionar la ubicación y el nombre del archivo
        nombre_archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
        if nombre_archivo:
            with open(nombre_archivo, "w") as archivo:
                archivo.write(codigo)
            messagebox.showinfo('Éxito',f'Contenido guardado exitosamente en {nombre_archivo}')

    #Si hay un archivo abierto en el compilador
    else:
        respuesta = messagebox.askyesno("Confirmación", "¿Estás seguro que deseas guardar los cambios?")
        if respuesta:
            
            with open(rutaFile, "w") as archivo:
                archivo.write(codigo)
            print("Contenido guardado exitosamente.")
            messagebox.showinfo('Éxito','Archivo guardado exitosamente')

    

def abrir_lenguaje(ruta):
    try:
        with open(ruta, 'r') as archivo:
            contenido = archivo.read()
        return contenido
    except FileNotFoundError:
        return "El archivo no existe."
    
def mostrar_lenguaje(ruta_archivo):
    # Crear ventana secundaria
    ventana_secundaria = tk.Toplevel(ventana)
    ventana_secundaria.title("LENGUAJE COMPILADOR FOCUS")

    # Crear caja de texto con scrollbar
    caja_texto = scrolledtext.ScrolledText(ventana_secundaria, wrap="word")
    caja_texto.pack(expand=True, fill="both")

    # Obtener contenido del archivo
    contenido = abrir_lenguaje(ruta_archivo)

    # Insertar contenido en la caja de texto
    caja_texto.insert(tk.END, contenido)
    

def limpiar_codigo():
    cajaCodigo.delete(1.0, tk.END)
    global rutaFile
    rutaFile = ""

def limpiar_consola():
    cajaConsola.delete(1.0, tk.END)
    cajaConsola.insert("end", "FOCUS-bash> ")


def colorear_palabras():
    text = cajaCodigo.get("1.0", tk.END)
    #Recorre el codigo buscando palabras del diccionario de colores
    for word_list, color in wordColors.items():
        for word in word_list:
            start_index = '1.0'
            while True:
                start_index = cajaCodigo.search(word, start_index, tk.END)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(word)}c"
                cajaCodigo.tag_add(color, start_index, end_index)
                start_index = end_index
    
    # Expresión regular para números enteros y decimales
    number_regex = r'\b\d+(\.\d+)?\b'
    matches = re.finditer(number_regex, text)
    for match in matches:
        start = f'1.0+{match.start()}c'
        end = f'1.0+{match.end()}c'
        cajaCodigo.tag_add('red', start, end)
    
    # Expresión regular para textos entre comillas
    quoted_text_regex = r'"[^"]*"'
    matches = re.finditer(quoted_text_regex, text)
    for match in matches:
        start = f'1.0+{match.start()}c'
        end = f'1.0+{match.end()}c'
        cajaCodigo.tag_add('green', start, end)
        
    # Expresión regular para líneas que comienzan con "!!" que sean comentarios
    lines = text.split("\n")
    for line_number, line in enumerate(lines):
        match = re.search(r'!!.*', line)
        if match:
            start_index = f"{line_number+1}.0"
            end_index = f"{line_number+1}.{match.end()}"
            cajaCodigo.tag_add("gray", start_index, end_index)

#Función que se ejecuta si se modifica el codigo
def cambia_texto(event):
    cajaCodigo.tag_remove("red", "1.0", tk.END)
    cajaCodigo.tag_remove("green", "1.0", tk.END)
    cajaCodigo.tag_remove("blue", "1.0", tk.END)
    cajaCodigo.tag_remove("yellow", "1.0", tk.END)
    cajaCodigo.tag_remove("gray", "1.0", tk.END)
    colorear_palabras()

#Función que se ejecuta al teclear en la consola Enter
def handle_key(event):
    if event.keysym == "Return":
        current_text = cajaConsola.get("end-2l linestart", "end-1c")
        process_input(current_text)
        cajaConsola.insert("end", "\nFOCUS-bash> ")
        cajaConsola.see("end")  # Hacer que el último texto sea visible
        return 'break'  # Para evitar que el comportamiento predeterminado de Tkinter maneje este evento

#Función para procesar lo escrito en la consola (comandos)
def process_input(input_text):
    # Obtener solo la última línea
    lines = input_text.strip().split('\n')
    last_line = lines[-1]    
    #print("Última línea ingresada:", last_line)
    patron = r'^FOCUS-bash>\s*(.*)$'
    # Buscar el patrón en cada cadena y extraer lo que sigue después de "FOCUS-bash>"
    resu = re.search(patron, last_line)
    if resu:
        comando = resu.group(1)
        print(comando)
    
        if comando == "clear":
            limpiar_consola()
        elif comando == "exit":
            ventana.destroy()
            



#--------------------- FUNCIONES DE LAS FASES DEL COMPILADOR -------------------------
def f1_Lexico():
    scrollConsole = tk.Scrollbar(ventana, orient=tk.VERTICAL)
    scrollConsole.place(x=913, y=545, height=150)
    cajaConsola = tk.Text(ventana, wrap=tk.WORD, yscrollcommand=scrollConsole.set, width=100, height=9,
                          font=('Source Code Pro', 10), bg="#4B4B4B", foreground="white", bd=None,
                          insertbackground="white")
    cajaConsola.place(x=107, y=546)
    scrollConsole.config(command=cajaConsola.yview)

    # Colocar el texto por defecto
    cajaConsola.insert("end", "FOCUS-bash> ")
    # Vincular eventos de teclado
    cajaConsola.bind("<KeyPress>", handle_key)

    lineaa = 1
    errores = 0
    #Comienza a verificar las palabras en el codigo

    inicio_fin=['.Start', '.Exit']


    contenido = []
    # Obtener el número total de líneas en la caja de texto
    num_lineas = int(cajaCodigo.index('end').split('.')[0])
    # Iterar sobre cada línea y obtener su contenido
    for i in range(1, num_lineas + 1):
        contenido.append(cajaCodigo.get(f"{i}.0", f"{i}.end"))

    for linea in contenido:
        if len(linea)>0: #comprobar si hay algo en la linea
            if (linea[0]=="!" and linea[1]=="!") or (linea in inicio_fin): #detectar si es un comentario o si es palabra de inicio o fin
                errores+=0
            elif "=" in linea: #sucede cuando es la asignacion de una variable
                partes = linea.split("=")
                variable = partes[0].strip()
                contVariable = partes[1].strip().replace(" ", "")

                #identificar error en identificadores
                if variable.startswith("set "):
                    variable = variable[len("set "):]
                erVariables=r'^[a-zA-Z_][a-zA-Z0-9_]*$'
                if re.match(erVariables, variable):
                    errores+=0
                else:
                    errores+=1
                    cajaConsola.insert("end", "Lexical error: Line "+str(lineaa)+" in identifier "+variable, "rojo")
                    cajaConsola.tag_configure("rojo", foreground="red")

                #identificar error en numeros
                num=""
                caracteres=list(contVariable)
                for i in range(len(caracteres)):
                    if caracteres[i].isdigit():
                        num+=caracteres[i]
                        if i>0:
                            if caracteres[i - 1] not in ['+', '-', '*', '/', '(', '.'] and not caracteres[i - 1].isdigit() and not re.match(erVariables, caracteres[i - 1]):
                                num=""
                                num=caracteres[i - 1]+caracteres[i]
                                errores += 1
                                cajaConsola.insert("end",
                                                   "Lexical error: Line " + str(lineaa) + " in wrong number " + num,
                                                   "rojo")
                                cajaConsola.tag_configure("rojo", foreground="red")
                                break
                        if i<len(caracteres)-1:
                            if caracteres[i + 1] not in ['+', '-', '*', '/', ')', '.', ';'] and not caracteres[i + 1].isdigit():
                                if re.match(erVariables, caracteres[i + 1]) and not re.match(erVariables, caracteres[i - 1]):
                                    num+=caracteres[i + 1]
                                    errores += 1
                                    cajaConsola.insert("end",
                                                       "Lexical error: Line " + str(lineaa) + " in wrong number " + num,
                                                       "rojo")
                                    cajaConsola.tag_configure("rojo", foreground="red")
                                    break
                    else:
                        if caracteres[i]=='.':
                            num+=caracteres[i]
                        else:
                            num=""

        else:
            errores += 0
        lineaa += 1
        if errores > 0:
            break
    
    '''
    for linea in contenido:
        print(f"Linea {l}: {linea}")
        l+=1'''


    # Lista de palabras reservadas
    palabras_reservadas = [".Start", ".Exit", "int", "flag", "char", "str", "float", "Show", ".input", "set", "true", "false"]

    # Función para limpiar la palabra de paréntesis y caracteres interiores
    def limpiar_palabra(palabra):
        palabra_limpia = palabra.rstrip(';')
        partes = palabra_limpia.split('(')
        if len(partes) > 1:
            return partes[0]
        else:
            return palabra_limpia

    l = 1
    for linea in contenido:
        palabras_linea = linea.split()  # Separar la línea en palabras
        for palabra in palabras_linea:
            palabra_limpia = limpiar_palabra(palabra)
            sugerencias = difflib.get_close_matches(palabra_limpia, palabras_reservadas, cutoff=0.6)
            if sugerencias:
                if sugerencias[0] != palabra_limpia:
                    #print(f"Error en la palabra reservada '{palabra}' en la línea {l}. ¿Quisiste decir '{sugerencias[0]}'?")
                    errores += 1
                    cajaConsola.insert("end",
                                        "Lexical error: Line " + str(l) + " in wrong reserved word " + palabra + f"  ¿Did you mean '{sugerencias[0]}'?",
                                        "rojo")
                    cajaConsola.tag_configure("rojo", foreground="red")
        l += 1


        

    if errores == 0:
        generarTabla = False
    else:
        generarTabla = True
        #Continua en el proceso de hacer la tabla de Tokens

def f2_sintatico():
    pass

def f3_semantico():
    pass

def f4_codInter():
    pass

def f5_Optimiza():
    pass

def f6_codObj():
    pass





# Crear la ventana principal
ventana = tk.Tk()
ventana.title("COMPILADOR FOCUS")
ventana.geometry("1280x720-100-100")
ventana.config(bg="#222222")
ventana.resizable(width=False,height=False)

styleBtn = ("Source Code Pro",10)
styleBtn2 = ("LED Dot-Matrix", 15)

#Título del compilador
nombreCompi = tk.Label(ventana,text="Compilador FOCUS",bg="#222222",foreground="white",font=("LED Dot-Matrix", 30))
nombreCompi.place(x=422,y=21)

#Caja de texto para el código
scrollCodigo = tk.Scrollbar(ventana, orient=tk.VERTICAL)
scrollCodigo.place(x=913,y=90, height=418)
cajaCodigo = tk.Text(ventana, wrap=tk.WORD, yscrollcommand=scrollCodigo.set, width=100,height=26, font=('Source Code Pro', 10),bg="#151515",foreground="white",bd=None,insertbackground="white")
cajaCodigo.place(x=107,y=88)
scrollCodigo.config(command=cajaCodigo.yview)

#Caja de texto para la consola
scrollConsole = tk.Scrollbar(ventana, orient=tk.VERTICAL)
scrollConsole.place(x=913,y=545, height=150)
cajaConsola = tk.Text(ventana, wrap=tk.WORD, yscrollcommand=scrollConsole.set,width=100,height=9, font=('Source Code Pro', 10),bg="#4B4B4B",foreground="white",bd=None,insertbackground="white")
cajaConsola.place(x=107,y=546)
scrollConsole.config(command=cajaConsola.yview)

# Colocar el texto por defecto
cajaConsola.insert("end", "FOCUS-bash> ")
# Vincular eventos de teclado
cajaConsola.bind("<KeyPress>", handle_key)

# Ligar el evento de cambio de texto para resaltar las palabras mientras se escribe
cajaCodigo.bind("<KeyRelease>", lambda event: colorear_palabras())
cajaCodigo.bind("<KeyRelease>", cambia_texto)

# Diccionario de listas de palabras y colores correspondientes
wordColors = {
    ('.Start', '.Exit'): "#6DC559",
    ('str', 'flag', 'int', 'char', 'float', '(', ')','.', ';'): "#F1E54A",
    ('true', 'false','Show', '<<', 'set', 'input'): "#4C90D4",
    ('=', '+', '-', '*', '/'): "#E56464"
}

# Crear etiquetas de estilo para resaltar las palabras
for color in set(wordColors.values()):
    cajaCodigo.tag_configure(color, foreground=color)
    
cajaCodigo.tag_configure('green', foreground='#6DC559')
cajaCodigo.tag_configure('blue', foreground='#4C90D4')
cajaCodigo.tag_configure('yellow', foreground='#F1E54A')
cajaCodigo.tag_configure('red', foreground='#E56464')
cajaCodigo.tag_configure('gray', foreground='#B5B5B5')




# Botón para abrir el archivo
img1 = Image.open('img/open.png')
img1.thumbnail((31,31),Image.ADAPTIVE)
imgOpen = ImageTk.PhotoImage(img1)
open_button = tk.Button(ventana, image=imgOpen, command=abrir_archivo,bg="#222222",bd=0)
open_button.place(x=107,y=50)

#Aquí se guardará la ruta del archivo que se haya abierto en caso de
global rutaFile
rutaFile = ""

#Botón para guardar el archivo
img2 = Image.open('img/save.png')
img2.thumbnail((31,31),Image.ADAPTIVE)
imgSave = ImageTk.PhotoImage(img2)
open_button = tk.Button(ventana,image=imgSave, command=guardar_archivo,bg="#222222",bd=0)
open_button.place(x=147,y=50)

#Botón para abrir el lenguaje
img3 = Image.open('img/lang.png')
img3.thumbnail((31,31),Image.ADAPTIVE)
imgCode = ImageTk.PhotoImage(img3)
botonLenguaje = tk.Button(ventana, image=imgCode, command=lambda:mostrar_lenguaje("lang.txt"),bg="#222222",bd=0)
botonLenguaje.place(x=197,y=50)

#Botón para limpiar el código
btnClearCodigo = tk.Button(ventana,text="CLEAR",font=styleBtn,bg="#B5B5B5",foreground="#000",command=limpiar_codigo)
btnClearCodigo.place(x=247,y=55)

#Botón para limpiar la consola
btnClearCodigo = tk.Button(ventana,text="CLEAR",font=styleBtn,bg="#B5B5B5",foreground="#000",command=limpiar_consola)
btnClearCodigo.place(x=880,y=518)



#--------------------------BOTONES DE LAS FASES DEL COMPILADOR ------------------------------------------------------

#Color verde de los botones #6DCB5A
#Color rojo de los botones #E74747
btnLexico = tk.Button(ventana,font=styleBtn2,command=f1_Lexico,text="LEXICO",width=12,height=2,bd=0,bg="#B5B5B5",foreground="white")
btnLexico.place(x=947,y=88)

btnSintactico = tk.Button(ventana,font=styleBtn2,command=f2_sintatico,text="SINTACTICO",width=12,height=2,bd=0,bg="#B5B5B5",foreground="white")
btnSintactico.place(x=947,y=149)

btnSemant = tk.Button(ventana,font=styleBtn2,command=f3_semantico,text="SEMANTICO",width=12,height=2,bd=0,bg="#B5B5B5",foreground="white")
btnSemant.place(x=947,y=209)

btnCodInter = tk.Button(ventana,font=styleBtn2,command=f4_codInter,text="CODIGO\nINTERMEDIO",width=12,height=2,bd=0,bg="#B5B5B5",foreground="white")
btnCodInter.place(x=947,y=269)

btnOptimiza = tk.Button(ventana,font=styleBtn2,command=f5_Optimiza,text="OPTIMIZACION",width=12,height=2,bd=0,bg="#B5B5B5",foreground="white")
btnOptimiza.place(x=947,y=329)

btnCodObj = tk.Button(ventana,font=styleBtn2,command=f6_codObj,text="CODIGO\nOBJETO",width=12,height=2,bd=0,bg="#B5B5B5",foreground="white")
btnCodObj.place(x=947,y=389)






# Iniciar la aplicación
ventana.mainloop()
