import tkinter as tk

app = tk.Tk()
app.title("Alineación Horizontal")
func = tk.StringVar(app)
val = tk.StringVar(app)
a = tk.StringVar(app)
b = tk.StringVar(app)
rango = tk.StringVar(app)
# Etiqueta
label = tk.Label(app, text="f(x)")
label.grid(row=0, column=0, padx=5, pady=5)

# Entrada de texto
entry_func = tk.Entry(app, textvariable=func)
entry_func.grid(row=0, column=1, padx=5, pady=5)

# Rango
label = tk.Label(app, text="Datos para calcular el rango")
label.grid(row=1, column=0, padx=5, pady=5)

label = tk.Label(app, text="a:")
label.grid(row=2, column=0, padx=5, pady=5)

entry_a = tk.Entry(app, textvariable=a)
entry_a.grid(row=2, column=1, padx=5, pady=5)

label = tk.Label(app, text="b:")
label.grid(row=2, column=2, padx=5, pady=5)

entry_b = tk.Entry(app, textvariable=b)
entry_b.grid(row=2, column=3, padx=5, pady=5)

label = tk.Label(app, text="rango:")
label.grid(row=2, column=4, padx=5, pady=5)

entry_r = tk.Entry(app, textvariable=rango)
entry_r.grid(row=2, column=5, padx=5, pady=5)

# Tamaño de población
label = tk.Label(app, text="tamaño de población")
label.grid(row=3, column=0, padx=5, pady=5)

label_inicial = tk.Label(app, text="Inicial:")
label_inicial.grid(row=4, column=0, padx=5, pady=5)

spinbox_min = tk.Spinbox(app, from_=1, to=10)
spinbox_min.grid(row=4, column=1, padx=5, pady=5) 

label_maximo = tk.Label(app, text="Máximo:")
label_maximo.grid(row=4, column=2, padx=5, pady=5)

spinbox_max = tk.Spinbox(app, from_=1, to=10,)
spinbox_max.grid(row=4, column=3, padx=5, pady=5)

# Probabilidades de mutación
label = tk.Label(app, text="Probabilidades de mutación")
label.grid(row=5, column=0, padx=5, pady=5)

label_individuo = tk.Label(app, text="Por individuo:")
label_individuo.grid(row=6, column=0, padx=5, pady=5)

entry_individuo = tk.Entry(app)
entry_individuo.grid(row=6, column=1, padx=5, pady=5)

label_gen = tk.Label(app, text="Por gen:")
label_gen.grid(row=6, column=2, padx=5, pady=5)

entry_gen = tk.Entry(app)
entry_gen.grid(row=6, column=3, padx=5, pady=5)

# Probabiidad de cruze
label = tk.Label(app, text="Probabilidades de cruze")
label.grid(row=7, column=0, padx=5, pady=5)

entry_cruze = tk.Entry(app)
entry_cruze.grid(row=7, column=1, padx=5, pady=5)

#Guardar los datos obtenidos
def print_entries():
    result = float(entry_b.get()) - float(entry_a.get())
    entry_r.delete(0, tk.END)
    entry_r.insert(0, str(result))
    entry_r.config(state="readonly")
    print("f(x):", func.get())
    print("a:", a.get())
    print("b:", b.get())
    print("rango:", rango.get())
    inicial = float(spinbox_min.get())/100
    print("Tamaño de población - Inicial:", inicial)
    maximo = float(spinbox_max.get())/100
    print("Tamaño de población - Máximo:", maximo)
    p_ind = float(entry_individuo.get())/100
    print("Probabilidades de mutación - Por individuo:", p_ind)
    p_gen = float(entry_gen.get())/100
    print("Probabilidades de mutación - Por gen:", p_gen)
    p_cruze = float(entry_cruze.get())/100
    print("Probabilidades de cruze:", p_cruze)

def create_window():
    new_window = tk.Tk()
    # Add widgets and configure the new window here
    new_window.title("Alineación Horizontal")
    new_window.mainloop()

def new_window():
    print_entries()
    app.destroy()
    create_window()

# Button to perform subtraction
button_end = tk.Button(app, text="Ejecutar algoritmo", command=new_window)
button_end.grid(row=8, column=2, padx=5, pady=5)

app.mainloop()
