import tkinter as tk
import random
from sympy import sympify

app = tk.Tk()
app.title("Alineación Horizontal")
func = tk.StringVar(app)
val = tk.StringVar(app)
a = tk.StringVar(app)
b = tk.StringVar(app)
rango = tk.StringVar(app)
bits = tk.StringVar(app)

# Widgets
# Función
label = tk.Label(app, text="f(x)")
label.grid(row=0, column=0, padx=5, pady=5)

entry_func = tk.Entry(app, textvariable=func)
entry_func.grid(row=0, column=1, padx=5, pady=5)

# Rangos de posibles soluciones
label = tk.Label(app, text="Rango")
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

label = tk.Label(app, text="Saltos")
label.grid(row=7, column=2, padx=5, pady=5)

entry_saltos = tk.Entry(app, textvariable=val)
entry_saltos.grid(row=7, column=3, padx=5, pady=5)

label = tk.Label(app, text="Numero de bits")
label.grid(row=7, column=4, padx=5, pady=5)

entry_bits = tk.Entry(app, textvariable=bits)
entry_bits.grid(row=7, column=5, padx=5, pady=5)

# Guardar los datos obtenidos
def print_entries():
    result = float(entry_b.get()) - float(entry_a.get())
    entry_r.delete(0, tk.END)
    entry_r.insert(0, str(result))
    entry_r.config(state="readonly")
    print("f(x):", func.get())
    print("a:", a.get())
    print("b:", b.get())
    print("rango:", rango.get())
    print("Tamaño de población - Inicial:", spinbox_min.get())
    print("Tamaño de población - Máximo:", spinbox_max.get())
    p_ind = float(entry_individuo.get())/100
    print("Probabilidades de mutación - Por individuo:", p_ind)
    p_gen = float(entry_gen.get())/100
    print("Probabilidades de mutación - Por gen:", p_gen)
    p_cruze = float(entry_cruze.get())/100
    print("Probabilidades de cruze:", p_cruze)
    number = int(entry_saltos.get())
    bits = len(bin(number-1)[2:])
    entry_bits.insert(0, str(bits))
    entry_bits.config(state="readonly")
    print(f"Number of bits needed: " , bits)

def new_window():
    new_window = tk.Tk()
    new_window.title("Alineación Horizontal")
    new_window.mainloop()

def generate_random_numbers(inicial):
    bits_needed = int(entry_bits.get())
    number = int(entry_saltos.get())
    num=(number-1)
    rango_value = float(entry_r.get())
    a = float(entry_a.get())
    print("a", a, "bits_needed:", num)
    numbers = []
    for i in range(inicial):
        number = random.randint(1,30)
        binary_representation = bin(number)[2:].zfill(bits_needed)  # Convertir a binario 
        deltax = float(rango_value / num)
        x = round(calculate_x(a, number, deltax), 3)
        print(f"i: {number}, c: {deltax}, x: {x}") 

        numbers.append({"id": i+1, "number": number, "binary": binary_representation,"x": x})
    return numbers

def calculate_x(a, number, deltax):
    return a + number * deltax

def print_entries_and_create_new_window():
    parsed_function = parse_function()

    if parsed_function is not None:
        print_entries()
        inicial = int(spinbox_min.get())
        numbers = generate_random_numbers(inicial)

        print("\nNúmeros generados y sus representaciones binarias:")
        for entry in numbers:
            print(f"ID: {entry['id']}, Number: {entry['number']}, Binary: {entry['binary']}, X: {entry['x']}, f(x): {parsed_function.subs('x', entry['x'])}")
    app.destroy()
    
def parse_function():
    try:
        function_str = func.get()
        sympified_function = sympify(function_str)
        return sympified_function
    except:
        print("Error al analizar la función. Asegúrate de que la función sea válida.")
        return None
# Botón para ejecutar el algoritmo
button_end = tk.Button(app, text="Ejecutar algoritmo", command=print_entries_and_create_new_window)
button_end.grid(row=8, column=3, padx=5, pady=5)

app.mainloop()
