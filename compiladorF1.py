import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import messagebox
import re
import time
import difflib

import sys
sys.setrecursionlimit(2000)

class RegexMatcher:
    def __init__(self, pattern):
        self.pattern = pattern

    def __eq__(self, other):
        return re.match(self.pattern, other) is not None

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
    # print("Ruta: ",rutaFile)
    codigo = cajaCodigo.get("1.0", tk.END)
    # Si no se abrió un archivo y se comenzó a codificar
    if rutaFile == "":
        # Abrir un cuadro de diálogo para seleccionar la ubicación y el nombre del archivo
        nombre_archivo = filedialog.asksaveasfilename(defaultextension=".txt",
                                                      filetypes=[("Archivos de texto", "*.txt")])
        if nombre_archivo:
            with open(nombre_archivo, "w") as archivo:
                archivo.write(codigo)
            messagebox.showinfo('Éxito', f'Contenido guardado exitosamente en {nombre_archivo}')

    # Si hay un archivo abierto en el compilador
    else:
        respuesta = messagebox.askyesno("Confirmación", "¿Estás seguro que deseas guardar los cambios?")
        if respuesta:
            with open(rutaFile, "w") as archivo:
                archivo.write(codigo)
            print("Contenido guardado exitosamente.")
            messagebox.showinfo('Éxito', 'Archivo guardado exitosamente')


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
    # Recorre el codigo buscando palabras del diccionario de colores
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
            start_index = f"{line_number + 1}.0"
            end_index = f"{line_number + 1}.{match.end()}"
            cajaCodigo.tag_add("gray", start_index, end_index)


# Función que se ejecuta si se modifica el codigo
def cambia_texto(event):
    cajaCodigo.tag_remove("red", "1.0", tk.END)
    cajaCodigo.tag_remove("green", "1.0", tk.END)
    cajaCodigo.tag_remove("blue", "1.0", tk.END)
    cajaCodigo.tag_remove("yellow", "1.0", tk.END)
    cajaCodigo.tag_remove("gray", "1.0", tk.END)
    colorear_palabras()


# Función que se ejecuta al teclear en la consola Enter
def handle_key(event):
    if event.keysym == "Return":
        current_text = cajaConsola.get("end-2l linestart", "end-1c")
        process_input(current_text)
        cajaConsola.insert("end", "\nFOCUS-bash> ")
        cajaConsola.see("end")  # Hacer que el último texto sea visible
        return 'break'  # Para evitar que el comportamiento predeterminado de Tkinter maneje este evento


# Función para procesar lo escrito en la consola (comandos)
def process_input(input_text):
    # Obtener solo la última línea
    lines = input_text.strip().split('\n')
    last_line = lines[-1]
    # print("Última línea ingresada:", last_line)
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


# --------------------- FUNCIONES DE LAS FASES DEL COMPILADOR -------------------------
def f1_Lexico():
    btnLexico.config(bg="#6DCB5A")
    btnSintactico.config(bg="#E74747")
    btnSemant.config(bg="#E74747")
    btnCodInter.config(bg="#E74747")
    btnOptimiza.config(bg="#E74747")
    btnCodObj.config(bg="#E74747")

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

    # Comienza a verificar las palabras en el codigo
    contenido = []
    # Obtener el número total de líneas en la caja de texto
    num_lineas = int(cajaCodigo.index('end').split('.')[0])
    # Iterar sobre cada línea y obtener su contenido
    for i in range(1, num_lineas + 1):
        contenido.append(cajaCodigo.get(f"{i}.0", f"{i}.end"))

    # Forma para imprimir en la consola
    '''
    cajaConsola.insert("end", "Lexical error: Line " + str(lineaa) + "contenido",
                                           "rojo")
                        cajaConsola.tag_configure("rojo", foreground="red")

    '''

    inicio_fin = ['.Start', '.Exit']

    for linea in contenido:
        if len(linea) > 0:  # comprobar si hay algo en la linea
            if (linea[0] == "!" and linea[1] == "!") or (
                    linea in inicio_fin):  # detectar si es un comentario o si es palabra de inicio o fin
                errores += 0
            elif "=" in linea and not linea.startswith('Show('):  # sucede cuando es la asignacion de una variable
                partes = linea.split("=")
                variable = partes[0].strip()
                variable = re.findall(r'\b(?:\d+\.\d+|\d+|\+\+|--|\+|\-|\*|\/|\(|\))\b|\S+', variable)
                contVariable = partes[1].strip()
                contVariable = re.findall(r'\b(?:\d+\.\d+|\d+|\+\+|--|\+|\-|\*|\/|\(|\))\b|\S+', contVariable)

                # identificar error en identificadores
                erVariables = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
                if len(variable) > 1:
                    if variable[0] == "set":
                        varrr = variable[1]
                    else:
                        errores += 1
                        cajaConsola.insert("end",
                                           "Lexical error: Line " + str(lineaa) + " in identifier " + variable[0] +
                                           variable[1],
                                           "rojo")
                        cajaConsola.tag_configure("rojo", foreground="red")
                        break
                else:
                    varrr = variable[0]
                if re.match(erVariables, varrr):
                    errores += 0
                else:
                    errores += 1
                    cajaConsola.insert("end", "Lexical error: Line " + str(lineaa) + " in identifier " + varrr, "rojo")
                    cajaConsola.tag_configure("rojo", foreground="red")

                # identificar error en numeros
                caracteres = contVariable
                operadores = ['+', '-', '*', '/', '(', ')']
                patron = r'^".*"$'
                patron2 = r"\d"
                patron3 = r'int\((.*?)\)'
                patron4 = r'float\((.*?)\)'
                for i in range(len(caracteres)):
                    match = re.search(patron3, caracteres[i])
                    if match:
                        caracteres[i] = match.group(1)
                        if not caracteres[i].isdigit() and caracteres[i] != "":
                            errores += 1
                            cajaConsola.insert("end",
                                               "Lexical error: Line " + str(lineaa) + " in wrong number " + caracteres[
                                                   i],
                                               "rojo")
                            cajaConsola.tag_configure("rojo", foreground="red")
                            break
                    match = re.search(patron4, caracteres[i])
                    if match:
                        caracteres[i] = match.group(1)
                    caracteres[i] = caracteres[i].replace(";", "")
                    if caracteres[i].isdigit() or caracteres[i] in operadores or re.match(erVariables,
                                                                                          caracteres[i]) or re.match(
                            patron, caracteres[i]) is not None or re.search(patron2, caracteres[i]) is None:
                        errores += 0
                    else:
                        partes = caracteres[i].split('.')
                        if len(partes) != 2:
                            decimal = False
                        elif partes[0].isdigit() and partes[1].isdigit():
                            decimal = True
                        else:
                            decimal = False
                        if decimal == False:
                            errores += 1
                            cajaConsola.insert("end",
                                               "Lexical error: Line " + str(lineaa) + " in wrong number " + caracteres[
                                                   i],
                                               "rojo")
                            cajaConsola.tag_configure("rojo", foreground="red")
                            break

                # identificar error en operadores
                opsIncorrectos = r'\*{3}|\+\+|--|\*{2}|\+\+|\*\+|/\*|\*/|/[-+]'
                for i in range(len(caracteres)):
                    if re.match(opsIncorrectos, caracteres[i]):
                        errores += 1
                        cajaConsola.insert("end",
                                           "Lexical error: Line " + str(lineaa) + " in operator " + caracteres[i],
                                           "rojo")
                        cajaConsola.tag_configure("rojo", foreground="red")
                        break



        else:
            errores += 0
        lineaa += 1
        if errores > 0:
            break

    # Lista de palabras reservadas
    palabras_reservadas = [".Start", ".Exit", "int", "flag", "char", "str", "float", "Show", ".input", "set",
                           "true", "false"]

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
                    # print(f"Error en la palabra reservada '{palabra}' en la línea {l}. ¿Quisiste decir '{sugerencias[0]}'?")
                    errores += 1
                    cajaConsola.insert("end",
                                       "Lexical error: Line " + str(
                                           l) + " in wrong reserved word " + palabra + f"  ¿Did you mean '{sugerencias[0]}'?",
                                       "rojo")
                    cajaConsola.tag_configure("rojo", foreground="red")
        l += 1

    # Función para limpiar la palabra de paréntesis y caracteres interiores
    def limpiar_palabra2(palabra):
        palabra_limpia = palabra.rstrip(';')
        partes = palabra_limpia.split('(')
        if len(partes) > 1:
            palabra_sin_parentesis = partes[1].split(')')[0]  # Obtener el contenido dentro de los paréntesis
            return palabra_sin_parentesis
        else:
            return palabra_limpia

    if errores == 0:
        l = 1
        for linea in contenido:
            palabras_linea = linea.split()  # Separar la línea en palabras
            for palabra in palabras_linea:
                palabra_limpia = limpiar_palabra2(palabra)
                sugerencias = difflib.get_close_matches(palabra_limpia, palabras_reservadas, cutoff=0.6)
                if sugerencias:
                    if sugerencias[0] != palabra_limpia:
                        # print(f"Error en la palabra reservada '{palabra}' en la línea {l}. ¿Quisiste decir '{sugerencias[0]}'?")
                        errores += 1
                        cajaConsola.insert("end",
                                           "Lexical error: Line " + str(
                                               l) + " in wrong reserved word " + palabra + f"  ¿Did you mean '{sugerencias[0]}'?",
                                           "rojo")
                        cajaConsola.tag_configure("rojo", foreground="red")

    if errores >= 1:
        generarTabla = False
    else:
        generarTabla = True
        # Continua en el proceso de hacer la tabla de Tokens
        tokens = []
        declares = []
        references = []
        l = 1
        for linea in contenido:
            if len(linea) > 0 and (linea[0] == "!" and linea[1] == "!"):
                linea = '!!'
            conct = False

            if linea.startswith('Show('):
                tr = ['Show', '(', ')', ';']
                for t in tr:
                    a = [t, l]
                    if not t in tokens:
                        tokens.append(t)
                        declares.append(a)
                    else:
                        references.append(a)
                    if t == '(':
                        patronShow = r'Show\((.*?)\)'
                        resultado = re.search(patronShow, linea)
                        if resultado:
                            contenido_show = resultado.group(1)
                            if '"' in contenido_show:
                                tc = '"'
                                a = [tc, l]
                                if not tc in tokens:
                                    tokens.append(tc)
                                    declares.append(a)
                                else:
                                    references.append(a)
                            if '<<' in contenido_show:
                                tc = ['<<']
                                partes = contenido_show.split("<< ", 1)
                                if len(partes) > 1:
                                    contenido_despues_de_ = partes[1]
                                    tc.append(contenido_despues_de_)
                                for tcc in tc:
                                    a = [tcc, l]
                                    if not tcc in tokens:
                                        tokens.append(tcc)
                                        declares.append(a)
                                    else:
                                        references.append(a)
                linea = ''

            tok = re.findall(r'\b(?:\d+\.\d+|\d+|\+\+|--|\+|\-|\*|\/|\(|\))\b|\S+', linea)
            for t in tok:
                aPC = False
                if t.endswith(';'):
                    t4 = ';'
                    aPC = [t4, l]
                    t = t[:-1]
                if t.startswith('"'):
                    t = '"'
                    a = [t, l]
                    if not t in tokens:
                        tokens.append(t)
                        declares.append(a)
                    else:
                        references.append(a)
                elif t.startswith('int().input('):
                    tr = ['int', '(', ')', '.input', '"', ';']
                    for t in tr:
                        a = [t, l]
                        if not t in tokens:
                            tokens.append(t)
                            declares.append(a)
                        else:
                            references.append(a)
                    break
                elif t.startswith('float().input('):
                    tr = ['float', '(', ')', '.input', '"', ';']
                    for t in tr:
                        a = [t, l]
                        if not t in tokens:
                            tokens.append(t)
                            declares.append(a)
                        else:
                            references.append(a)
                    break
                elif t.startswith('char().input('):
                    tr = ['char', '(', ')', '.input', '"', ';']
                    for t in tr:
                        a = [t, l]
                        if not t in tokens:
                            tokens.append(t)
                            declares.append(a)
                        else:
                            references.append(a)
                    break
                elif t.startswith('str().input('):
                    tr = ['str', '(', ')', '.input', '"', ';']
                    for t in tr:
                        a = [t, l]
                        if not t in tokens:
                            tokens.append(t)
                            declares.append(a)
                        else:
                            references.append(a)
                    break
                elif t.startswith('int('):
                    tr = ['int', '(', ')']
                    for t2 in tr:
                        a = [t2, l]
                        if not t2 in tokens:
                            tokens.append(t2)
                            declares.append(a)
                        else:
                            references.append(a)
                        if t2 == '(':
                            match = re.search(r'int\((\d+)\)', t)
                            if match:
                                t3 = match.group(1)
                                a = [t3, l]
                                if not t3 in tokens:
                                    tokens.append(t3)
                                    declares.append(a)
                                else:
                                    references.append(a)
                elif t.startswith('float('):
                    tr = ['float', '(', ')']
                    for t2 in tr:
                        a = [t2, l]
                        if not t2 in tokens:
                            tokens.append(t2)
                            declares.append(a)
                        else:
                            references.append(a)
                        if t2 == '(':
                            match = re.search(r'float\(([\d.]+)\)', t)
                            if match:
                                t3 = match.group(1)
                                a = [t3, l]
                                if not t3 in tokens:
                                    tokens.append(t3)
                                    declares.append(a)
                                else:
                                    references.append(a)

                elif t.startswith('flag('):
                    tr = ['flag', '(', ')']
                    for t2 in tr:
                        a = [t2, l]
                        if not t2 in tokens:
                            tokens.append(t2)
                            declares.append(a)
                        else:
                            references.append(a)
                        if t2 == '(':
                            match = re.search(r'flag\((true|false)\)', t)
                            if match:
                                t3 = match.group(1)
                                a = [t3, l]
                                if not t3 in tokens:
                                    tokens.append(t3)
                                    declares.append(a)
                                else:
                                    references.append(a)
                elif t.startswith('str('):
                    tr = ['str', '(', ')']
                    for t2 in tr:
                        a = [t2, l]
                        if not t2 in tokens:
                            tokens.append(t2)
                            declares.append(a)
                        else:
                            references.append(a)
                elif t.startswith('char('):
                    tr = ['char', '(', ')']
                    for t2 in tr:
                        a = [t2, l]
                        if not t2 in tokens:
                            tokens.append(t2)
                            declares.append(a)
                        else:
                            references.append(a)

                elif t != '':
                    a = [t, l]
                    if not t in tokens:
                        tokens.append(t)
                        declares.append(a)
                    else:
                        references.append(a)

                if aPC:
                    if not t4 in tokens:
                        tokens.append(t4)
                        declares.append(aPC)
                    else:
                        references.append(aPC)

            l += 1

        datos = []
        palabras_reservadas2 = [".Start", ".Exit", "int", "flag", "char", "str", "float", "Show",
                                ".input", "set",
                                "true", "false"]
        erVariables = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
        operadores = ['+', '-', '*', '/', '=']
        contTokens = 0
        for t in tokens:
            reference = [""]
            if t in palabras_reservadas2:
                tipo = 'Palabra reservada'
            elif re.match(erVariables, t):
                tipo = 'Identificador'
            elif t in operadores:
                tipo = 'Operador'
            else:
                tipo = 'Carácter'
            for r in references:
                if t == r[0]:
                    reference.append(r[1])
            if len(reference) > 1:
                reference.pop(0)
            dato = [t, tipo, declares[contTokens][1], reference]
            datos.append(dato)
            contTokens += 1

        ventanaTabla = tk.Toplevel(ventana)
        columnas = ("Token", "Type", "Declares", "Reference")
        style = ttk.Style()
        style.configure("Treeview", font=('Helvetica', 8), rowheight=25, fieldbackground='light gray')
        style.configure("Treeview.Heading", font=('Helvetica', 9))
        tabla = ttk.Treeview(ventanaTabla, style="Treeview")
        tabla["show"] = "headings"
        tabla.pack(expand=True, fill=tk.BOTH)
        tabla["columns"] = columnas
        for col in columnas:
            tabla.heading(col, text=col)

        for dato in datos:
            tabla.insert("", tk.END, values=dato)


def f2_sintatico():
    btnLexico.config(bg="#E74747")
    btnSintactico.config(bg="#6DCB5A")
    btnSemant.config(bg="#E74747")
    btnCodInter.config(bg="#E74747")
    btnOptimiza.config(bg="#E74747")
    btnCodObj.config(bg="#E74747")

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

    cajaConsola.tag_configure("azul", background="white", foreground="#0000FF", font=("Helvetica", 10, "bold"))  # Fondo azul claro, texto azul
    cajaConsola.tag_configure("amarillo", background="white",
                              foreground="#FFA500", font=("Helvetica", 10, "bold"))  # Fondo amarillo claro, texto dorado
    cajaConsola.tag_configure("rojo", background="white", foreground="#FF4500", font=("Helvetica", 10, "bold"))  # Fondo rojo claro, texto rojo oscuro
    cajaConsola.tag_configure("verde", background="white", foreground="#008000", font=("Helvetica", 10, "bold"))  # Fondo verde claro, texto verde
    cajaConsola.tag_configure("blanco", foreground="white")


    # ------------- Gramática---------------------------------------------------------------------------------------------------------------------
    num = [[RegexMatcher(r"^-?\d+$")]]
    dec = [[RegexMatcher(r"^-?\d+(\.\d+)?$")]]
    Vfloat = [[dec], ['']]
    nomVar = [[RegexMatcher(r"^[a-zA-Z_][a-zA-Z0-9_]*$")]]
    Conct = [[nomVar], ['"', '"'], [num], [dec]]
    Concatenar = [[nomVar, '=', Conct, '<<', Conct, ';']]
    Ope = [[RegexMatcher(r'^\s*(?:[+-]?\d+(\.\d+)?|[a-zA-Z][a-zA-Z0-9]*)\s*(?:[+\-*/]\s*([+-]?\d+(\.\d+)?|[a-zA-Z][a-zA-Z0-9]*))*\s*$')]]
    Operacion = [[nomVar, '=', Ope, ';']]
    Dato = [[num], [dec], ['true'], ['false'], ['"', '"']]
    Mostrar = [['Show', '(', Conct, ')', ';'], ['Show', '(', Conct, '<<', Conct, ')', ';']]
    tipoDato = [['int', '(', ')'], ['float', '(', ')'], ['char', '(', ')'], ['str', '(', ')']]
    IngresarDato = [[nomVar, '=', tipoDato, '.input', '(', '"', '"', ')', ';']]
    VariableVariable = [['set', nomVar, '=', nomVar, ';']]
    AsignaValor = [[nomVar, '=', Dato, ';']]
    Vflag = [['true'], ['false'], ['']]
    Vint = [[num], ['']]
    tipo = [['int', '(', Vint, ')'], ['str', '(', ')'], ['char', '(', ')'], ['flag', '(', Vflag, ')'],
            ['float', '(', Vfloat, ')']]
    DeclaraVar = [[nomVar, '=', tipo, ';']]
    Linea = [["!!"], [VariableVariable], [Mostrar], [Operacion], [IngresarDato], [DeclaraVar], [AsignaValor], [Concatenar]]
    F = [[".Start", Linea, ".Exit"]]

    # ----------------------------------------------------------------------------------

    # Comienza a verificar las palabras en el codigo
    contenido = []
    # Obtener el número total de líneas en la caja de texto
    num_lineas = int(cajaCodigo.index('end').split('.')[0])
    # Iterar sobre cada línea y obtener su contenido
    for i in range(1, num_lineas + 1):
        contenido.append(cajaCodigo.get(f"{i}.0", f"{i}.end"))

    tokens = []
    operadores = ['+', '-', '*', '/']
    opecad=""
    for linea in contenido:

        if len(linea) > 0 and (linea[0] == "!" and linea[1] == "!"):
            linea = '!!'
        conct = False

        if linea.startswith('Show(') and linea.endswith(');'):
            tr = ['Show', '(', ')', ';']
            for t in tr:
                tokens.append(t)
                if t == '(':
                    patronShow = r'Show\((.*?)\)'
                    resultado = re.search(patronShow, linea)
                    if resultado:
                        contenido_show = resultado.group(1)
                        tok = re.findall(r'"[^"]*"|\b(?:\d+\.\d+|\d+|\+\+|--|\+|\-|\*|\/|\(|\))\b|\S+', contenido_show)
                        for t in tok:
                            if t.startswith('"') and t.endswith('"'):
                                t = '"'
                                tokens.append(t)
                                tokens.append(t)
                            elif t != '':
                                tokens.append(t)

            linea = ''

        tok = re.findall(r'"[^"]*"|\b(?:\d+\.\d+|\d+|\+\+|--|\+|\-|\*|\/|\(|\))\b|\S+', linea)
        for t in tok:
            aPC = False
            if t.endswith(';') and not t.startswith('int().') and not t.startswith('float().') and not t.startswith('char().') and not t.startswith('str().'):
                t4 = ';'
                aPC = t4
                t = t[:-1]
            if t.startswith('"') and t.endswith('"'):
                t = '"'
                tokens.append(t)
                tokens.append(t)
            elif t.startswith('int().input("') and t.endswith('");'):
                tr = ['int', '(', ')', '.input', '(', '"', '"', ')', ';']
                for t in tr:
                    tokens.append(t)
                break
            elif t.startswith('float().input("') and t.endswith('");'):
                tr = ['float', '(', ')', '.input', '(', '"', '"', ')', ';']
                for t in tr:
                    tokens.append(t)
                break
            elif t.startswith('char().input("') and t.endswith('");'):
                tr = ['char', '(', ')', '.input', '(', '"', '"', ')', ';']
                for t in tr:
                    tokens.append(t)
                break
            elif t.startswith('str().input("') and t.endswith('");'):
                tr = ['str', '(', ')', '.input', '(', '"', '"', ')', ';']
                for t in tr:
                    tokens.append(t)
                break
            elif t.startswith('int(') and t.endswith(')') and not t.startswith('int()i'):
                tr = ['int', '(', ')']
                for t2 in tr:
                    tokens.append(t2)
                    if t2 == '(':
                        match = re.search(r'int\((.*?)\)', t)
                        if match:
                            t3 = match.group(1)
                            tokens.append(t3)
                        else:
                            tokens.append('')
            elif t.startswith('float(') and t.endswith(')') and not t.startswith('float()i'):
                tr = ['float', '(', ')']
                for t2 in tr:
                    tokens.append(t2)
                    if t2 == '(':
                        match = re.search(r'float\((.*?)\)', t)
                        if match:
                            t3 = match.group(1)
                            tokens.append(t3)
                        else:
                            tokens.append('')

            elif t.startswith('flag(') and t.endswith(')') and not t.startswith('flag()i'):
                tr = ['flag', '(', ')']
                for t2 in tr:
                    tokens.append(t2)
                    if t2 == '(':
                        match = re.search(r'flag\((.*?)\)', t)
                        if match:
                            t3 = match.group(1)
                            tokens.append(t3)
                        else:
                            tokens.append('')
            elif t.startswith('str(') and t.endswith(')') and not t.startswith('str()i'):
                tr = ['str', '(', ')']
                for t2 in tr:
                    tokens.append(t2)
            elif t.startswith('char(') and t.endswith(')') and not t.startswith('char()i'):
                tr = ['char', '(', ')']
                for t2 in tr:
                    tokens.append(t2)

            elif t != '':
                if opecad == "":
                    if len(tokens)>0:
                        if t in operadores:
                            opecad=opecad+tokens[-1]+t
                            tokens.pop()
                        else:
                            tokens.append(t)
                    else:
                        tokens.append(t)
                else:
                    opecad = opecad + t

            if aPC:
                if opecad!="":
                    tokens.append(opecad)
                    opecad=""
                tokens.append(t4)

    tokens.append('#')
    print(tokens)
    def lista_a_str(elemento, nombres_variables):
        if isinstance(elemento, list):
            for nombre, valor in nombres_variables.items():
                if valor is elemento:
                    return nombre
            return "[" + ", ".join(lista_a_str(sub_elem, nombres_variables) for sub_elem in elemento) + "]"
        elif isinstance(elemento, RegexMatcher):
            if elemento.pattern == r"^-?\d+$":
                return 'ER Enteros'
            elif elemento.pattern == r"^-?\d+(\.\d+)?$":
                return 'ER Decimales'
            elif elemento.pattern == r"^[a-zA-Z_][a-zA-Z0-9_]*$":
                return 'ER Variables'
            elif elemento.pattern == r'^\s*(?:[+-]?\d+(\.\d+)?|[a-zA-Z][a-zA-Z0-9]*)\s*(?:[+\-*/]\s*([+-]?\d+(\.\d+)?|[a-zA-Z][a-zA-Z0-9]*))*\s*$':
                return 'ER Operaciones'
            else:
                return 'Expresión Regular'
        else:
            return str(elemento)

    nombres_variables = {
        'F': F,
        'Linea': Linea,
        'DeclaraVar': DeclaraVar,
        'tipo': tipo,
        'Vint': Vint,
        'Vflag': Vflag,
        'AsignaValor': AsignaValor,
        'Dato': Dato,
        'VariableVariable': VariableVariable,
        'IngresarDato': IngresarDato,
        'tipoDato': tipoDato,
        'Mostrar': Mostrar,
        'Operacion': Operacion,
        'Ope': Ope,
        'Concatenar': Concatenar,
        'Conct': Conct,
        'nomVar': nomVar,
        'Vfloat': Vfloat,
        'num': num,
        'dec': dec
    }
    est=['n', 1, [], [F, '#']]
    est_strs = [lista_a_str(elem, nombres_variables) for elem in est]
    cajaConsola.insert("end", "\n" + ",".join(est_strs), "blanco")
    cajaConsola.insert("end", "\n" + "Expansión del arbol", "blanco")
    est = ['n', 1, [[F]], ['.Exit', '#']]
    for i in range(len(contenido)-1):
        if contenido[i]!='' and contenido[i]!='.Start' and contenido[i]!='.Exit':
            est[3].insert(0, Linea)
    est[3].insert(0, '.Start')

    terminales = list(nombres_variables.keys())

    def obtener_nombre(valor, nombres_variables):
        for nombre, variable in nombres_variables.items():
            if variable is valor:
                return nombre
        return None

    est_strs = [lista_a_str(elem, nombres_variables) for elem in est]
    cajaConsola.insert("end", "\n" + ",".join(est_strs), "blanco")

    def proceso(est, exp):
        if exp==1:
            est[0]='n'
            est[1]=est[1]
            est[2].append([est[3][0], 0])
            NT=est[3][0][0]
            est[3].pop(0)
            for i in reversed(NT):
                est[3].insert(0, i)
            cajaConsola.insert("end", "\n" + "Expansión del arbol" + "\n", "blanco")

        elif exp==2:
            est[0] = 'n'
            est[1] = est[1]+1
            est[2].append(est[3][0])
            est[3].pop(0)
            cajaConsola.insert("end", "\n" + "Concordancia de un simbolo" + "\n", "blanco")

        elif exp==3:
            est[0] = 't'
            est[1] = est[1]+1
            est[2]=est[2]
            est[3]=''
            cajaConsola.insert("end", "\n" + "Terminación con exito" + "\n", "blanco")

        elif exp==4:
            est[0] = 'r'
            est[1] = est[1]
            est[2]=est[2]
            est[3]=est[3]
            cajaConsola.insert("end", "\n" + "No concordancia de un simbolo" + "\n", "blanco")

        elif exp==5:
            est[0] = 'r'
            est[1] = est[1]-1
            est[3].insert(0, est[2][-1])
            est[2].pop()
            cajaConsola.insert("end", "\n" + "Retroceso a la entrada" + "\n", "blanco")

        elif exp==60:
            est[0] = 'n'
            est[1] = est[1]
            for i in est[2][-1][0][est[2][-1][1]]:
                est[3].pop(0)
            est[2][-1][1] = est[2][-1][1]+1
            for i in reversed(est[2][-1][0][est[2][-1][1]]):
                est[3].insert(0, i)
            cajaConsola.insert("end", "\n" + "Siguiente alternativa A" + "\n", "blanco")

        elif exp==61:
            est[0] = 'e'
            cajaConsola.insert("end", "\n" + "Siguiente alternativa B" + "\n", "blanco")

        elif exp==62:
            est[0] = 'r'
            est[1] = est[1]
            for i in est[2][-1][0][est[2][-1][1]]:
                est[3].pop(0)
            est[3].insert(0, est[2][-1][0])
            est[2].pop()
            cajaConsola.insert("end", "\n" + "Siguiente alternativa C" + "\n", "blanco")

        est_strs = [lista_a_str(elem, nombres_variables) for elem in est]
        colores = ["azul", "amarillo", "rojo", "verde"]
        for i, est_str in enumerate(est_strs):
            color_tag = colores[i % len(colores)]
            cajaConsola.insert("end", est_str, color_tag)
            if i < len(est_strs) - 1:
                cajaConsola.insert("end", ",", "blanco")


        if est[0] == 'n':
            if tokens[est[1]-1]==est[3][0]:
                if est[3][0]=='#':
                    proceso(est, 3)
                else:
                    proceso(est, 2)
            elif isinstance(est[3][0], list):
                nombre_terminal = obtener_nombre(est[3][0], nombres_variables)
                if nombre_terminal in terminales:
                    proceso(est, 1)
            else:
                proceso(est, 4)
        elif est[0] == 'r':
            if isinstance(est[2][-1], list):
                if est[2][-1][0] == F:
                    proceso(est, 61)
                elif len(est[2][-1][0])>1:
                    if est[2][-1][1]+1==len(est[2][-1][0]):
                        proceso(est, 62)
                    else:
                        proceso(est, 60)
                else:
                    proceso(est, 62)
            else:
                proceso(est, 5)
        elif est[0]=='t':
            print("Terminación con exito")
        elif est[0]=='e':
            print("Error")

    if tokens[est[1] - 1] == est[3][0]:
        if est[3][0] == '#':
            proceso(est, 3)
        else:
            proceso(est, 2)
    else:
        proceso(est, 4)




def f3_semantico():
    
    # ------------- Gramática---------------------------------------------------------------------------------------------------------------------
    num = [[RegexMatcher(r"^-?\d+$")]]
    dec = [[RegexMatcher(r"^-?\d+(\.\d+)?$")]]
    Vfloat = [[dec], ['']]
    nomVar = [[RegexMatcher(r"^[a-zA-Z_][a-zA-Z0-9_]*$")]]
    Conct = [[nomVar], ['"', '"'], [num], [dec]]
    Concatenar = [[nomVar, '=', Conct, '<<', Conct, ';']]
    Ope = [[RegexMatcher(r'^\s*(?:[+-]?\d+(\.\d+)?|[a-zA-Z][a-zA-Z0-9]*)\s*(?:[+\-*/]\s*([+-]?\d+(\.\d+)?|[a-zA-Z][a-zA-Z0-9]*))*\s*$')]]
    Operacion = [[nomVar, '=', Ope, ';']]
    Dato = [[num], [dec], ['true'], ['false'], ['"', '"']]
    Mostrar = [['Show', '(', Conct, ')', ';'], ['Show', '(', Conct, '<<', Conct, ')', ';']]
    tipoDato = [['int', '(', ')'], ['float', '(', ')'], ['char', '(', ')'], ['str', '(', ')']]
    IngresarDato = [[nomVar, '=', tipoDato, '.input', '(', '"', '"', ')', ';']]
    VariableVariable = [['set', nomVar, '=', nomVar, ';']]
    AsignaValor = [[nomVar, '=', Dato, ';']]
    Vflag = [['true'], ['false'], ['']]
    Vint = [[num], ['']]
    tipo = [['int', '(', Vint, ')'], ['str', '(', ')'], ['char', '(', ')'], ['flag', '(', Vflag, ')'],
            ['float', '(', Vfloat, ')']]
    DeclaraVar = [[nomVar, '=', tipo, ';']]
    Linea = [["!!"], [VariableVariable], [Mostrar], [Operacion], [IngresarDato], [DeclaraVar], [AsignaValor], [Concatenar]]
    F = [[".Start", Linea, ".Exit"]]

    # ----------------------------------------------------------------------------------
    
    '''
    IDENTIFICADORES NO DEFINIDOS
    OPERANDOS INCOMPATIBLES
    VARIABLES DUPLICADAS
    
    - Si no hay errores mostrar TABLA SEMÁNTICA con atributo VALOR
    - Mostrar árbol semántico con atributo valor evaluado en cada nivel
      y por prioridad de operadores
    - Mostrar que tipo de error es y la linea donde se presentó (Opcional: Podría agregarse el fragmento de código ERROR)
    '''
    # Comienza a verificar las palabras en el codigo
    contenido = []
    # Obtener el número total de líneas en la caja de texto
    num_lineas = int(cajaCodigo.index('end').split('.')[0])
    # Iterar sobre cada línea y obtener su contenido
    for i in range(1, num_lineas + 1):
        contenido.append(cajaCodigo.get(f"{i}.0", f"{i}.end"))

    tokens = []
    operadores = ['+', '-', '*', '/']
    opecad=""
    
    
    
    


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
ventana.resizable(width=False, height=False)

styleBtn = ("Source Code Pro", 10)
styleBtn2 = ("LED Dot-Matrix", 15)

# Título del compilador
nombreCompi = tk.Label(ventana, text="Compilador FOCUS", bg="#222222", foreground="white", font=("LED Dot-Matrix", 30))
nombreCompi.place(x=422, y=21)

# Caja de texto para el código
scrollCodigo = tk.Scrollbar(ventana, orient=tk.VERTICAL)
scrollCodigo.place(x=913, y=90, height=418)
cajaCodigo = tk.Text(ventana, wrap=tk.WORD, yscrollcommand=scrollCodigo.set, width=100, height=26,
                     font=('Source Code Pro', 10), bg="#151515", foreground="white", bd=None, insertbackground="white")
cajaCodigo.place(x=107, y=88)
scrollCodigo.config(command=cajaCodigo.yview)

# Caja de texto para la consola
scrollConsole = tk.Scrollbar(ventana, orient=tk.VERTICAL)
scrollConsole.place(x=913, y=545, height=150)
cajaConsola = tk.Text(ventana, wrap=tk.WORD, yscrollcommand=scrollConsole.set, width=100, height=9,
                      font=('Source Code Pro', 10), bg="#4B4B4B", foreground="white", bd=None, insertbackground="white")
cajaConsola.place(x=107, y=546)
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
    ('str', 'flag', 'int', 'char', 'float', '(', ')', '.', ';'): "#F1E54A",
    ('true', 'false', 'Show', '<<', 'set', 'input'): "#4C90D4",
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
img1.thumbnail((31, 31), Image.ADAPTIVE)
imgOpen = ImageTk.PhotoImage(img1)
open_button = tk.Button(ventana, image=imgOpen, command=abrir_archivo, bg="#222222", bd=0)
open_button.place(x=107, y=50)

# Aquí se guardará la ruta del archivo que se haya abierto en caso de
global rutaFile
rutaFile = ""

# Botón para guardar el archivo
img2 = Image.open('img/save.png')
img2.thumbnail((31, 31), Image.ADAPTIVE)
imgSave = ImageTk.PhotoImage(img2)
open_button = tk.Button(ventana, image=imgSave, command=guardar_archivo, bg="#222222", bd=0)
open_button.place(x=147, y=50)

# Botón para abrir el lenguaje
img3 = Image.open('img/lang.png')
img3.thumbnail((31, 31), Image.ADAPTIVE)
imgCode = ImageTk.PhotoImage(img3)
botonLenguaje = tk.Button(ventana, image=imgCode, command=lambda: mostrar_lenguaje("lang.txt"), bg="#222222", bd=0)
botonLenguaje.place(x=197, y=50)

# Botón para limpiar el código
btnClearCodigo = tk.Button(ventana, text="CLEAR", font=styleBtn, bg="#B5B5B5", foreground="#000",
                           command=limpiar_codigo)
btnClearCodigo.place(x=247, y=55)

# Botón para limpiar la consola
btnClearCodigo = tk.Button(ventana, text="CLEAR", font=styleBtn, bg="#B5B5B5", foreground="#000",
                           command=limpiar_consola)
btnClearCodigo.place(x=880, y=518)

# --------------------------BOTONES DE LAS FASES DEL COMPILADOR ------------------------------------------------------

# Color verde de los botones #6DCB5A
# Color rojo de los botones #E74747
btnLexico = tk.Button(ventana, font=styleBtn2, command=f1_Lexico, text="LEXICO", width=12, height=2, bd=0, bg="#B5B5B5",
                      foreground="white")
btnLexico.place(x=947, y=88)

btnSintactico = tk.Button(ventana, font=styleBtn2, command=f2_sintatico, text="SINTACTICO", width=12, height=2, bd=0,
                          bg="#B5B5B5", foreground="white")
btnSintactico.place(x=947, y=149)

btnSemant = tk.Button(ventana, font=styleBtn2, command=f3_semantico, text="SEMANTICO", width=12, height=2, bd=0,
                      bg="#B5B5B5", foreground="white")
btnSemant.place(x=947, y=209)

btnCodInter = tk.Button(ventana, font=styleBtn2, command=f4_codInter, text="CODIGO\nINTERMEDIO", width=12, height=2,
                        bd=0, bg="#B5B5B5", foreground="white")
btnCodInter.place(x=947, y=269)

btnOptimiza = tk.Button(ventana, font=styleBtn2, command=f5_Optimiza, text="OPTIMIZACION", width=12, height=2, bd=0,
                        bg="#B5B5B5", foreground="white")
btnOptimiza.place(x=947, y=329)

btnCodObj = tk.Button(ventana, font=styleBtn2, command=f6_codObj, text="CODIGO\nOBJETO", width=12, height=2, bd=0,
                      bg="#B5B5B5", foreground="white")
btnCodObj.place(x=947, y=389)

# Iniciar la aplicación
ventana.mainloop()
