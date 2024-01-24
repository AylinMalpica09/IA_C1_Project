import tkinter as tk
import math as math
import random
import cv2 
from sympy import lambdify, sympify
from sympy import symbols, log, cos, Abs, sympify
import matplotlib.pyplot as plt
import os
import numpy as np
#rutas
ruta_images = "/Users/ventu/Escritorio/IA_C1_Project/images"
ruta_final = "/Users/ventu/Escritorio/IA_C1_Project/"
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
    print("fx: ",funcion.get())
    print("Población incial: ",po_inicial.get())
    print("Población máximma: ",po_max.get())
    print("Probabilidad de muta individual: ",p_ind.get())
    print("Probabilidad de muta generación: ",p_gen.get())
    print("X máxima: ",x_max.get())
    print("X mínima: ",x_min.get())
    print("Número de iteraciones: ",iteraciones.get())
    print("Número de resoluciones: ",resolucion.get())
    print("Valor del boton: ",opcion)

label = tk.Label(app, text="fx")
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

iteraciones = tk.Spinbox(app, from_=1, to=100,textvariable=iteraciones)
iteraciones.grid(row=10, column=1, padx=5, pady=5)

label_maximo = tk.Label(app, text="Resolución deseada")
label_maximo.grid(row=10, column=2, padx=5, pady=5)

resolucion = tk.Spinbox(app, from_=0, to=1,textvariable=resolucion)
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
    
    bits_needed = get_bits()
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
    #Calculamos el rango 
    bits_final = math.ceil(bits)
    #print ("bits final: ", bits_final)
    return bits_final

def generate_indiv(bits_needed):
    global parsed_function 
    parsed_function = parse_function()
    
    if parsed_function is not None:
        numbers = generate_p0(bits_needed)
       
    return numbers

def generate_p0(bits_needed):
    global parsed_function 
    parsed_function = parse_function()

    tamaño = int(po_inicial.get())
    min_x = float(x_min.get())
    max_x = float(x_max.get())
    rango_value = int(max_x - min_x)

    num = int((2**(bits_needed)) - 1)
    number_bits = (2**(bits_needed))
    list = []

    for i in range(tamaño):
        number = random.randint(1, number_bits)
        binary_representation = bin(number)[2:].zfill(bits_needed)  # Convertir a binario 
        deltax = float(rango_value / num)
        x = round(calculate_x(min_x, number, deltax), 4)
       
        fx = round(parsed_function.subs('x', x), 4)
        list.append({"id": i+1, "number": number, "binary": binary_representation, "x": x, "fx": fx})

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
#optimizacion  

def optimizacion(ind):
    generaciones = int(iteraciones.get())
    resultados_grafica = []
    mejor_global = {}  # Inicializar mejor_global como un diccionario vacío
    poblacion_total = organizar(ind)
    for generacion in range(generaciones):
        #print(f"\nProceso de optimización - Generación {generacion}\n")
        id_gen = generacion
        
       
        ultimo_id = len(poblacion_total)
        parejas_formada = parejas(poblacion_total)
        parejas_cruzadas = cruza(parejas_formada, ultimo_id)
        gen_mutada = mutacion(parejas_cruzadas)
        poblacion_total = poblacion_total + gen_mutada
        #
        
        datos,best,worst = obtener_datos_generacion(poblacion_total)
        if opcion ==1:
            mejor_local = min(poblacion_total, key=lambda entry: entry['fx'])

      
            if not mejor_global or mejor_local['fx'] < mejor_global['fx']:
                mejor_global = mejor_local.copy() 

            resultados_grafica.append({
                "mejor": mejor_global['fx'],
                "promedio": get_promedio(poblacion_total),
                "peor": max(poblacion_total, key=lambda entry: entry['fx'])['fx']
            })
        elif opcion ==2:
            
            mejor_local = max(poblacion_total, key=lambda entry: entry['fx'])

           
            if not mejor_global or mejor_local['fx'] > mejor_global['fx']:
                mejor_global = mejor_local.copy() 

            resultados_grafica.append({
                "mejor": mejor_global['fx'],
                "promedio": get_promedio(poblacion_total),
                "peor": min(poblacion_total, key=lambda entry: entry['fx'])['fx']
            })
        plot_resultados_gen(datos, best, worst,id_gen)
        gen_podada = poda(poblacion_total)
        poblacion_total = gen_podada

    print("soy el mejor individuo:", mejor_global)
    plot_resultados(resultados_grafica)
    crear_video(ruta_images)
    return resultados_grafica

def organizar (ind):
    numbers_org = []
    if opcion == 1:
        numbers_org = sorted(ind, key=lambda entry: parsed_function.subs('x', entry['x']))
    elif opcion ==2:
        numbers_org = sorted(ind, key=lambda entry: parsed_function.subs('x', entry['x']), reverse=True)
  
    return numbers_org

def parejas (ind_ordenados):
    # Obtener la mejor mitad de la población para la cruza
    best_half = ind_ordenados[:len(ind_ordenados)//2]
    return best_half

def cruza(parejas_formada,ultimo_id):
    #datos inicales
    min_x = float(x_min.get())
    max_x = float(x_max.get())
    rango_value = int (max_x - min_x)
    num = int (2**(bits_final)-1)
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
        new_generation.append({"id": ultimo_id + len(new_generation) + 1, "number": child_number_1, "binary": child_binary_1, "x": child_x_1, "fx": child_fx_1})
        new_generation.append({"id": ultimo_id + len(new_generation) + 1, "number": child_number_2, "binary": child_binary_2, "x": child_x_2, "fx": child_fx_2})
    return new_generation

def mutacion (parejas_cruzadas):  
    prob_gen = float(p_gen.get())
    
    for entry in parejas_cruzadas:
        entry['mutation_value'] = round(random.uniform(0, 100) / 100, 3) 
    mutacion = parejas_cruzadas
    # Filtrar los individuos que mutarán (cuyo valor de mutación es menor a p_ind)
    mutated_candidates = [entry for entry in mutacion if entry['mutation_value'] < float(p_ind.get())]  
   
    mutated_individuals = [mutacion_ind(entry, p_gen) for entry in mutated_candidates]
    # Actualizar los valores mutados en la lista original
    for mutated_individual in mutated_individuals:
        for i, entry in enumerate(mutacion):
            if entry['id'] == mutated_individual['id']:
                mutacion[i] = mutated_individual
                break
   
    return mutacion

def mutacion_ind(mutated_candidates, p_gen):
    min_x = float(x_min.get())
    max_x = float(x_max.get())
    rango_value = int(max_x - min_x)
    num = int(2**(bits_final) - 1)
    deltax = float(rango_value / num)  
    
    p_gen_value = float(p_gen.get())

    # Obtén la representación binaria del número
    binary_representation = bin(mutated_candidates['number'])[2:].zfill(bits_final)

    # Aplica la negación de bits con probabilidad p_gen
    mutated_binary = ''.join(['1' if random.uniform(0, 1) <= p_gen_value else '0' if bit == '1' else '1' for bit in binary_representation])

    # Crear un nuevo individuo mutado
    mutated_individual = mutated_candidates.copy()
    mutated_individual['id'] = mutated_individual['id']
    mutated_individual['binary'] = mutated_binary
    mutated_individual['number'] = int(mutated_individual['binary'], 2)
    mutated_individual['x'] = round(calculate_x(min_x, number=mutated_individual['number'], deltax=deltax), 3)
    mutated_individual['fx'] = parsed_function.subs('x', mutated_individual['x'])
    
    return mutated_individual

#grafica 
def grafica(gen_podada,resultados_grafica):
    print("vamos por los datos de la grafica\n")
    if opcion == 1:
        mejor = gen_podada[0]
        peor = max(gen_podada, key=lambda entry: entry['fx'])
        promedio = round(sum(entry['fx'] for entry in gen_podada) / len(gen_podada),4)
        print("Mejor valor de fx: {:.4f}".format(mejor['fx']))
        print("Promedio valor de fx:",promedio)
        print("Peor valor de fx: {:.4f}".format(peor['fx']))
        #guardamos los valores
        resultados_grafica.append({
            "mejor": mejor['fx'],
            "promedio": promedio,
            "peor": peor['fx']
        })
    elif opcion ==2:
        mejor = gen_podada[0]
        peor = min(gen_podada, key=lambda entry: entry['fx'])
        promedio = round(sum(entry['fx'] for entry in gen_podada) / len(gen_podada),4)
        print("Mejor valor de fx: {:.4f}".format(mejor['fx']))
        print("Promedio valor de fx:",promedio)
        print("Peor valor de fx: {:.4f}".format(peor['fx']))
        resultados_grafica.append({
            "mejor": mejor['fx'],
            "promedio": promedio,
            "peor": peor['fx']
        })
    return resultados_grafica

def org_pob_total (poblacion_total):
    min_x = float(x_min.get())
    max_x = float(x_max.get())
    rango_value = int(max_x - min_x)
    num = int(2**(bits_final) - 1)
    deltax = float(rango_value / num)  
    pob_total_order = []
    # Crear un conjunto para almacenar los números únicos
    numeros_unicos = set()
    # Recorrer la población original y agregar a la nueva lista solo si el número no está en el conjunto
    for entry in poblacion_total:
        if entry['number'] not in numeros_unicos:
            numeros_unicos.add(entry['number'])
            entry['x'] = round(calculate_x(min_x, number=entry['number'], deltax=deltax), 3)
            entry['fx'] = parsed_function.subs('x', entry['x'])
            pob_total_order.append(entry)
    if opcion == 1:
        
        pob_total_order = sorted(pob_total_order, key=lambda entry: parsed_function.subs('x', entry['x']))
    elif opcion ==2:
        
        pob_total_order = sorted(pob_total_order, key=lambda entry: parsed_function.subs('x', entry['x']), reverse=True)
    
    return pob_total_order

def poda(poblacion_total):
    po_max = int(p_max.get())
    
    poblacion = org_pob_total(poblacion_total)
     # Mantener al mejor individuo
    mejor_individuo=None
    peor_individuo=None
    if opcion == 1:
        mejor_individuo = min(poblacion, key=lambda entry: entry['fx'])
        peor_individuo= max(poblacion, key=lambda entry: entry['fx'])
    elif opcion == 2:
        mejor_individuo = max(poblacion, key=lambda entry: entry['fx'])
        peor_individuo= min(poblacion, key=lambda entry: entry['fx'])

    nueva_poblacion = []
    nueva_poblacion.append(mejor_individuo)
    #nueva_poblacion.append(peor_individuo)
    
    cantidad_a_eliminar = max(0, len(poblacion) - po_max)
    
    indices_a_eliminar = random.sample(range(1, len(poblacion)), min(cantidad_a_eliminar, len(poblacion) - 1))
    
    nueva_poblacion.extend(entry for i, entry in enumerate(poblacion[1:], start=1) if i not in indices_a_eliminar)

    # Actualizar los IDs en la nueva población
    for i, entry in enumerate(nueva_poblacion, start=1):
        entry['id'] = i
   
    return nueva_poblacion

def get_promedio (poblacion):
    promedio = sum(entry['fx'] for entry in poblacion) / len(poblacion)
    return promedio

def start ():
    ind=data_inicial()
    optimizacion(ind)

def obtener_datos_generacion(poblacion_total):
    datos = []
   
    if opcion == 1:
        datos = sorted(poblacion_total, key=lambda entry: parsed_function.subs('x', entry['x']))
        mejor = datos[0]
        peor = max(datos, key=lambda entry: entry['fx'])


    elif opcion == 2:
        datos = sorted(poblacion_total, key=lambda entry: parsed_function.subs('x', entry['x']), reverse=True)
        mejor = datos[0]
        peor = min(datos, key=lambda entry: entry['fx'])


    return datos, mejor, peor

#grafica 
def plot_resultados(resultados_grafica,save_path=ruta_final):
    generaciones = range(len(resultados_grafica))
    mejor = [resultado['mejor'] for resultado in resultados_grafica]
    promedio = [resultado['promedio'] for resultado in resultados_grafica]
    peor = [resultado['peor'] for resultado in resultados_grafica]
    
    plt.plot(generaciones, mejor, label='Mejor')
    plt.plot(generaciones, promedio, label='Promedio')
    plt.plot(generaciones, peor, label='Peor')

    plt.xlabel('Generación')
    plt.ylabel('fx')
    plt.title('Resultados de las Generaciones')
    plt.legend()
    if save_path:
        # Asegurarse de que el directorio de guardado exista
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        filename = 'grafica final.png'
        plt.savefig(os.path.join(save_path, filename))
    plt.show()
    plt.close()
    
def plot_resultados_gen(datos, best, worst, id_gen, save_path=ruta_images):
    # print("generacion n°:", id_gen)
    datos_x = [i['x'] for i in datos]
    datos_y = [i['fx'] for i in datos]
    # print(datos_x, datos_y)

    # Generar valores de x para la curva de la función
    x_vals = np.linspace(float(x_min.get()), float(x_max.get()), 100)
    # Calcular los valores correspondientes de f(x) para la curva
    y_vals = [parsed_function.subs('x', x_val) for x_val in x_vals]

    plt.scatter(datos_x, datos_y, label='Individuos')
    plt.scatter(best['x'], best['fx'], label='Mejor')
    plt.scatter(worst['x'], worst['fx'], label='Peor')
    plt.plot(x_vals, y_vals, label='f(x)') 

    plt.xlim(float(x_min.get()), float(x_max.get()))

    plt.xlabel('Generación')
    plt.ylabel('fx')
    plt.title('Resultado de la Generacion {}'.format(id_gen))
    plt.suptitle('f(x)= {}'.format(funcion.get()))
    plt.legend()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        filename = 'resultado_generacion_{}.png'.format(id_gen)
        plt.savefig(os.path.join(save_path, filename))
    else:
        plt.show()

    plt.close()

#generar videos
def crear_video(images, nombre_video="video_resultados.mp4", fps=1):
    imagenes = [img for img in os.listdir(images) if img.endswith(".png")]
    imagenes_ordenadas = sorted(imagenes, key=lambda x: int(x.split('_')[-1].split('.')[0]))

    frame = cv2.imread(os.path.join(images, imagenes[0]))
    altura, ancho, _ = frame.shape

    video = cv2.VideoWriter(nombre_video, cv2.VideoWriter_fourcc(*"mp4v"), fps, (ancho, altura))

    for imagen in imagenes_ordenadas:
        frame = cv2.imread(os.path.join(images, imagen))
        video.write(frame)

    cv2.destroyAllWindows()
    video.release()

    print(f"El video {nombre_video} ha sido creado con éxito.")

button_end = tk.Button(app, text="Ejecutar algoritmo", command=start)
button_end.grid(row=12, column=1, padx=5, pady=5)    

app.mainloop()
