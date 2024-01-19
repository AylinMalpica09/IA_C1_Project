import tkinter as tk
import math as math
import random
from sympy import lambdify, sympify

app = tk.Tk()
app.title("Proyecto IA C1")

#Valores
funcion = tk.StringVar(app)
po_inicial = tk.StringVar(app)
po_max = tk.StringVar(app)
p_ind = tk.StringVar(app)
p_gen = tk.StringVar(app)
x_max = tk.StringVar(app)
x_min = tk.StringVar(app)
iteraciones  = tk.StringVar(app)
resolucion  = tk.StringVar(app)
opcion = None

def print_entries(valor):
    global opcion
    opcion = valor
    print("f(x): ",funcion.get())
    print("Población incial: ",po_inicial.get())
    print("Población máximma: ",po_max.get())
    print("Probabilidad de muta individual: ",p_ind.get())
    print("Probabilidad de muta generación: ",p_gen.get())
    print("X máxima: ",x_max.get())
    print("X mínima: ",x_min.get())
    print("Número de iteraciones: ",iteraciones.get())
    print("Número de resoluciones: ",resolucion.get())
    print("Valor del boton: ",opcion)

label = tk.Label(app, text="f(x)")
label.grid(row=0, column=0, padx=5, pady=5)

funcion = tk.Entry(app, textvariable=funcion)
funcion.grid(row=0, column=1, padx=5, pady=5)

# Tamaño de población
label = tk.Label(app, text="Tamaño de población")
label.grid(row=3, column=0, padx=5, pady=5)

label_inicial = tk.Label(app, text="Inicial:")
label_inicial.grid(row=4, column=0, padx=5, pady=5)

p_inicial = tk.Spinbox(app, from_=1, to=10, textvariable=po_inicial)
p_inicial.grid(row=4, column=1, padx=5, pady=5)

label_maximo = tk.Label(app, text="Máximo:")
label_maximo.grid(row=4, column=2, padx=5, pady=5)

p_max = tk.Spinbox(app, from_=1, to=10,textvariable=po_max)
p_max.grid(row=4, column=3, padx=5, pady=5)

# Probabilidades de mutación
label = tk.Label(app, text="Probabilidades de mutación")
label.grid(row=5, column=0, padx=5, pady=5)

label_individuo = tk.Label(app, text="Por individuo:")
label_individuo.grid(row=6, column=0, padx=5, pady=5)

p_ind = tk.Entry(app, textvariable=p_ind)
p_ind.grid(row=6, column=1, padx=5, pady=5)

label_gen = tk.Label(app, text="Por gen:")
label_gen.grid(row=6, column=2, padx=5, pady=5)

p_gen = tk.Entry(app, textvariable=p_gen)
p_gen.grid(row=6, column=3, padx=5, pady=5)

# Rango de posibles soluciones
label = tk.Label(app, text="Rango de posibles soluciones")
label.grid(row=7, column=0, padx=5, pady=5)

label_maximo = tk.Label(app, text="Mínimo:")
label_maximo.grid(row=8, column=0, padx=5, pady=5)

x_min_entry = tk.Entry(app, textvariable=x_min)
x_min_entry.grid(row=8, column=1, padx=5, pady=5)

label_maximo = tk.Label(app, text="Máximo:")
label_maximo.grid(row=8, column=2, padx=5, pady=5)

x_max_entry = tk.Entry(app, textvariable=x_max)
x_max_entry.grid(row=8, column=3, padx=5, pady=5)

label_maximo = tk.Label(app, text="Iteraciones")
label_maximo.grid(row=10, column=0, padx=5, pady=5)

iteraciones = tk.Spinbox(app, from_=1, to=10,textvariable=iteraciones)
iteraciones.grid(row=10, column=1, padx=5, pady=5)

label_maximo = tk.Label(app, text="Resolución deseada")
label_maximo.grid(row=10, column=2, padx=5, pady=5)

resolucion = tk.Spinbox(app, from_=1, to=10,textvariable=resolucion)
resolucion.grid(row=10, column=3, padx=5, pady=5)
#Botones
button_min = tk.Button(app, text="Minimización", command=lambda:on_button_click(1))
button_min.grid(row=11, column=1, padx=5, pady=5)

button_min = tk.Button(app, text="Maximización", command=lambda:on_button_click(2))
button_min.grid(row=11, column=3, padx=5, pady=5)

#Funciones 

def on_button_click(valor):
    global opcion
    opcion = valor
     
def data_inicial ():
    bits_needed = get_bits() #calculo el numero de la repreesentacion de los bits
    print("numero de bits: ", bits_needed)
    ind = generate_indiv(bits_needed)
    return (ind)

def get_bits ():
    global bits_final
    min_x = float(x_min.get())
    max_x = float(x_max.get())
    rango = max_x - min_x
    saltos = rango/ float(resolucion.get())
    puntos = saltos + 1
    bits = float(math.log2(puntos))
    bits_final = math.ceil(bits)
    return bits_final

def generate_indiv(bits_needed):
    global parsed_function  # Hacer global la funcion
    parsed_function = parse_function()
    
    if parsed_function is not None:
        
        numbers = generate_p0(bits_needed)
        
        print("\nNúmeros generados y sus representaciones binarias:")
        for entry in numbers:
            print(f"ID: {entry['id']}, Number: {entry['number']}, Binary: {entry['binary']}, X: {entry['x']}, f(x): {parsed_function.subs('x', entry['x'])}")
    return numbers

def generate_p0 (bits_needed):
    tamaño = int(po_inicial.get())
    min_x = float(x_min.get())
    max_x = float(x_max.get())
    rango_value = int (max_x - min_x)
    num = int (2**(bits_needed))
    list = []
    for i in range(tamaño):
        number = random.randint(1, num)
        binary_representation = bin(number)[2:].zfill(bits_needed)  # Convertir a binario 
        deltax = float(rango_value / num)
        x = round(calculate_x(min_x, number, deltax), 3)
        #print(f"i: {number}, c: {deltax}, x: {x}") 

        list.append({"id": i+1, "number": number, "binary": binary_representation,"x": x})
    return list

def calculate_x(a, number, deltax):
    return a + number * deltax

def parse_function():
    try:
        function_str = funcion.get()
        sympified_function = sympify(function_str)
        return sympified_function
    except:
        print("Error al analizar la función. Asegúrate de que la función sea válida.")
        return None

def optimizacion (ind):
    print ("Proceso de optimización ")
    ind_ordenados = organizar(ind) #ordena mi p0 para minimizar o maximizar
    ultimo_id = len(ind_ordenados)
    parejas_formada = parejas(ind_ordenados)
    parejas_cruzadas=cruza(parejas_formada, ultimo_id)
    #print("parejas cruzadas: ",parejas_cruzadas)
    #print(cruza)
    return

def organizar (ind):
    numbers_org = []
    if opcion == 1:
        print("\nMinimizado")
        numbers_org = sorted(ind, key=lambda entry: parsed_function.subs('x', entry['x']))
    elif opcion ==2:
        print("\nMaximizado")
        numbers_org = sorted(ind, key=lambda entry: parsed_function.subs('x', entry['x']), reverse=True)
    print("\nNúmeros organizados y sus representaciones binarias:")
    for entry in numbers_org:
        print(f"ID: {entry['id']}, Number: {entry['number']}, Binary: {entry['binary']}, X: {entry['x']}, f(x): {parsed_function.subs('x', entry['x'])}")

    return numbers_org

def parejas (ind_ordenados):
    # Obtener la mejor mitad de la población para la cruza
    best_half = ind_ordenados[:len(ind_ordenados)//2]
    #print (best_half)
    return best_half

def cruza(parejas_formada,ultimo_id):
    
    print("estoy en la cruza\n Soy el ultimo ID:", ultimo_id)
    min_x = float(x_min.get())
    max_x = float(x_max.get())
    rango_value = int (max_x - min_x)
    num = int (2**(bits_final))
    deltax = float(rango_value / num)   
    
    best_individual = max(parejas_formada, key=lambda x: parsed_function.subs('x', x['x']))
    mejor_mitad = [individuo for individuo in parejas_formada if individuo != best_individual]
    punto_cruza = bits_final//2 + bits_final % 2
    new_generation = []

    for other_individual in mejor_mitad:
        
        child_binary_1 = best_individual['binary'][:punto_cruza] + other_individual['binary'][punto_cruza:]
        child_number_1 = int(child_binary_1, 2)
        child_x_1 = round(calculate_x(min_x, child_number_1, deltax), 3)
        child_fx_1 = parsed_function.subs('x', child_x_1)

        child_binary_2 = other_individual['binary'][:punto_cruza] + best_individual['binary'][punto_cruza:]
        child_number_2 = int(child_binary_2, 2)
        child_x_2 = round(calculate_x(min_x, child_number_1, deltax), 3)
        child_fx_2 = parsed_function.subs('x', child_x_2)
        # Agrega los nuevos individuos a la nueva generación
        new_generation.append({"id": ultimo_id + len(new_generation) + 1, "number": child_number_1, "binary": child_binary_1, "x": child_x_1, "f(x)": child_fx_1, "padre1": best_individual['id'], "padre2": other_individual['id']})
        new_generation.append({"id": ultimo_id + len(new_generation) + 1, "number": child_number_2, "binary": child_binary_2, "x": child_x_2, "f(x)": child_fx_2, "padre1": other_individual['id'], "padre2": best_individual['id']})
    print ("nueva generacion creada\n", new_generation)
    return new_generation

def start ():
    ind=data_inicial()
    optimizacion(ind)
    
button_end = tk.Button(app, text="Ejecutar algoritmo", command=start)
button_end.grid(row=12, column=1, padx=5, pady=5)    

app.mainloop()