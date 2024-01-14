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
        #print(f"i: {number}, c: {deltax}, x: {x}") 

        numbers.append({"id": i+1, "number": number, "binary": binary_representation,"x": x})
    return numbers

def calculate_x(a, number, deltax):
    return a + number * deltax

def print_entries_and_create_new_window():
    global parsed_function  # Hacer global para que sea accesible desde sort_and_crossover
    parsed_function = parse_function()

    if parsed_function is not None:
        print_entries()
        inicial = int(spinbox_min.get())
        numbers = generate_random_numbers(inicial)

        print("\nNúmeros generados y sus representaciones binarias:")
        for entry in numbers:
            print(f"ID: {entry['id']}, Number: {entry['number']}, Binary: {entry['binary']}, X: {entry['x']}, f(x): {parsed_function.subs('x', entry['x'])}")

        new_generation = sort_and_crossover(numbers)
    app.destroy()

def print_sorted_population(sorted_population):
    print("\nTabla ordenada por f(x):")
    print("{:<5} {:<10} {:<20} {:<10} {:<10} {:<10}".format("ID", "Number", "Binary", "X", "f(x)", "Mutado"))
    for entry in sorted_population:
        print("{:<5} {:<10} {:<20} {:<10} {:<10} {:<10}".format(entry['id'], entry['number'], entry['binary'], entry['x'], parsed_function.subs('x', entry['x']), entry.get('mutado', '-')))

def sort_and_crossover(numbers):
    # Ordenar la población por aptitud (evaluación de la función) de mayor a menor
    sorted_population = sorted(numbers, key=lambda x: parsed_function.subs('x', x['x']), reverse=True)

    print_sorted_population(sorted_population)

    # Obtener la mejor mitad de la población para la cruza
    best_half = sorted_population[:len(sorted_population)//2]

    # Verificar que haya suficientes individuos para la cruza
    if len(best_half) < 2:
        print("No hay suficientes individuos para realizar la cruza.")
        return []

    # Seleccionar aleatoriamente el mejor individuo de la mejor mitad
    best_individual = max(best_half, key=lambda x: parsed_function.subs('x', x['x']))

    print("\nIndividuo seleccionado aleatoriamente de la mejor mitad:")
    print(f"Mejor Individuo - ID: {best_individual['id']}, Number: {best_individual['number']}, Binary: {best_individual['binary']}, X: {best_individual['x']}, f(x): {parsed_function.subs('x', best_individual['x'])}")

    # Generar la nueva generación después de la cruza
    new_generation = []

    # Realizar la cruza con todos los demás individuos de la mejor mitad
    for other_individual in [entry for entry in best_half if entry != best_individual]:
        # Calcular el punto de cruza basado en el valor de a
        crossover_point = int(entry_a.get()) - 1

        # Realizar la primera cruza
        child_binary_1 = best_individual['binary'][:crossover_point] + other_individual['binary'][crossover_point:]
        child_number_1 = int(child_binary_1, 2)
        child_x_1 = round(calculate_x(a=float(entry_a.get()), number=child_number_1,
                                       deltax=float(entry_r.get()) / (int(entry_saltos.get()) - 1)), 3)
        child_fx_1 = parsed_function.subs('x', child_x_1)

        # Realizar la segunda cruza
        child_binary_2 = other_individual['binary'][:crossover_point] + best_individual['binary'][crossover_point:]
        child_number_2 = int(child_binary_2, 2)
        child_x_2 = round(calculate_x(a=float(entry_a.get()), number=child_number_2,
                                       deltax=float(entry_r.get()) / (int(entry_saltos.get()) - 1)), 3)
        child_fx_2 = parsed_function.subs('x', child_x_2)

        # Agregar los nuevos individuos a la nueva generación
        new_generation.append({"id": len(new_generation) + 1, "number": child_number_1, "binary": child_binary_1, "x": child_x_1, "f(x)": child_fx_1, "padre1": best_individual['id'], "padre2": other_individual['id']})
        new_generation.append({"id": len(new_generation) + 1, "number": child_number_2, "binary": child_binary_2, "x": child_x_2, "f(x)": child_fx_2, "padre1": other_individual['id'], "padre2": best_individual['id']})

        print("\nIndividuos generados después de la cruza:")
        print(f"Hijo 1 - Number: {child_number_1}, Binary: {child_binary_1}, X: {child_x_1}, f(x): {child_fx_1}, Padres: {best_individual['id']} y {other_individual['id']}")
        print(f"Hijo 2 - Number: {child_number_2}, Binary: {child_binary_2}, X: {child_x_2}, f(x): {child_fx_2}, Padres: {other_individual['id']} y {best_individual['id']}")
    
    p_ind = float(entry_individuo.get())/100  # Asegúrate de obtener el valor correcto
    p_gen = float(entry_gen.get())/100  # Asegúrate de obtener el valor correcto

    print(f"\nValor de p_ind: {p_ind}")
    print(f"\nValor de p_gen: {p_gen}")

    #print("aqui estoy xxxxxxxxxxxxxxxxxxx")
    new_generation_mutated = mutate_generation(new_generation, p_ind, p_gen)

    # Finalmente, muestra la nueva generación mutada
    print("\nNueva generación después de la mutación:")
    print_sorted_population(new_generation_mutated)

    return new_generation

def should_mutate(p_ind):
    # Evaluación del evento estocástico para la mutación
    return random.uniform(0, 100) < p_ind

def mutate_individual2(individual, p_ind, p_gen):
    # Obtener el valor de mutación
    mutation_value = random.uniform(0, 100) / 100
    print(f"\nMutación por bit para el individuo ID {individual['id']}:\n{mutation_value}")
    # Comparar el valor de mutación con la probabilidad de mutación por individuo
    if mutation_value <= p_ind:
        # Comparar la probabilidad de mutación generada con la probabilidad de mutación por generación
        mutation_generation_value = random.uniform(0, 100) / 100
        if mutation_generation_value <= p_gen:
            # Mutar el individuo (estrategia de Negación del bit)
            mutated_position = random.randint(0, len(individual['binary']) - 1)
            mutated_value = '0' if individual['binary'][mutated_position] == '1' else '1'

            # Crear un nuevo individuo mutado
            mutated_individual = individual.copy()
            mutated_individual['binary'] = individual['binary'][:mutated_position] + mutated_value + individual['binary'][mutated_position+1:]
            mutated_individual['number'] = int(mutated_individual['binary'], 2)
            mutated_individual['x'] = round(calculate_x(a=float(entry_a.get()), number=mutated_individual['number'],
                                                        deltax=float(entry_r.get()) / (int(entry_saltos.get()) - 1)), 3)
            mutated_individual['f(x)'] = parsed_function.subs('x', mutated_individual['x'])

            return mutated_individual
        else:
            # No mutar el individuo
            return individual
    else:
        # No mutar el individuo
        return individual
def mutate_individual(individual, p_ind, p_gen):
    # Obtener el valor de mutación por bit
    mutation_values = [random.uniform(0.1, 0.9) for _ in range(len(individual['binary']))]

    print(f"\nMutación por bit para el individuo ID {individual['id']}:\n{mutation_values}")

    # Comparar el valor de mutación por bit con la probabilidad de mutación por generación
    mutated_bits = [1 if mutation_values[i] <= p_gen else 0 for i in range(len(individual['binary']))]

    # Realizar la mutación de bits solo donde se cumple la probabilidad de mutación por generación
    mutated_binary = ''.join(['1' if mutated_bits[i] == 1 else original_bit for i, original_bit in enumerate(individual['binary'])])

    # Crear un nuevo individuo mutado
    mutated_individual = individual.copy()
    mutated_individual['binary'] = mutated_binary
    mutated_individual['number'] = int(mutated_individual['binary'], 2)
    mutated_individual['x'] = round(calculate_x(a=float(entry_a.get()), number=mutated_individual['number'],
                                                deltax=float(entry_r.get()) / (int(entry_saltos.get()) - 1)), 3)
    mutated_individual['f(x)'] = parsed_function.subs('x', mutated_individual['x'])
    
    print(f"Individuo mutado ID {individual['id']} después de la mutación:")
    print(f"Binary: {mutated_individual['binary']}, X: {mutated_individual['x']}, f(x): {mutated_individual['f(x)']}")

    return mutated_individual

def mutate_individual1(individual, p_ind, p_gen):
    # Obtener el valor de mutación por bit
    mutation_values = [random.uniform(0.1, 0.9) for _ in range(len(individual['binary']))]

    print(f"\nMutación por bit para el individuo ID {individual['id']}:\n{mutation_values}")

    # Comparar el valor de mutación por bit con la probabilidad de mutación por generación
    mutated_bits = [1 if mutation_values[i] <= p_gen else 0 for i in range(len(individual['binary']))]

    # Realizar la mutación de bits
    mutated_binary = ''.join([str(mutated_bits[i]) if mutated_bits[i] == 1 else individual['binary'][i] for i in range(len(individual['binary']))])

    # Crear un nuevo individuo mutado
    mutated_individual = individual.copy()
    mutated_individual['binary'] = mutated_binary
    mutated_individual['number'] = int(mutated_individual['binary'], 2)
    mutated_individual['x'] = round(calculate_x(a=float(entry_a.get()), number=mutated_individual['number'],
                                                deltax=float(entry_r.get()) / (int(entry_saltos.get()) - 1)), 3)
    mutated_individual['f(x)'] = parsed_function.subs('x', mutated_individual['x'])
    
    print(f"Individuo mutado ID {individual['id']} después de la mutación:")
    print(f"Binary: {mutated_individual['binary']}, X: {mutated_individual['x']}, f(x): {mutated_individual['f(x)']}")

    return mutated_individual
    
def print_sorted_population_with_id(sorted_population, title="Tabla ordenada por f(x)"):
    print(f"\n{title}:")
    print("{:<5} {:<5} {:<10} {:<20} {:<10} {:<10}".format("ID", "Mutado", "Number", "Binary", "X", "f(x)"))
    for entry in sorted_population:
        number_decimal = int(entry['binary'], 2)
        print("{:<5} {:<5} {:<10} {:<20} {:<10} {:<10}".format(entry['id'], "Sí" if entry['mutated'] else "No", number_decimal, entry['binary'], entry['x'], entry['f(x)']))

def mutate_generation(generation, p_ind, p_gen):

    print("estoy en la mutacion por generacion")
    # Asignar valor de mutación a cada individuo de la generación
    for entry in generation:
        entry['mutation_value'] = random.uniform(0, 100) / 100  # Dividir por 100

    # Mostrar todos los individuos y sus valores de mutación
    print("\nTodos los individuos despues de la cruza y sus valores de mutación:")
    print("{:<5} {:<10} {:<20} {:<10} {:<10} {:<15}".format("ID", "Number", "Binary", "X", "f(x)", "Mutation Value"))
    for entry in generation:
        print("{:<5} {:<10} {:<20} {:<10} {:<10} {:<15}".format(entry['id'], entry['number'], entry['binary'], entry['x'], entry['f(x)'], entry['mutation_value']))

    # Filtrar los individuos que mutarán (cuyo valor de mutación es menor a p_ind)
    mutated_candidates = [entry for entry in generation if entry['mutation_value'] < p_ind]

    # Mostrar los candidatos a mutación en una tabla
    print("\nCandidatos a mutación:")
    print("{:<5} {:<10} {:<20} {:<10} {:<10} {:<15}".format("ID", "Number", "Binary", "X", "f(x)", "Mutation Value"))
    for entry in mutated_candidates:
        print("{:<5} {:<10} {:<20} {:<10} {:<10} {:<15}".format(entry['id'], entry['number'], entry['binary'], entry['x'], entry['f(x)'], entry['mutation_value']))

    # Aplicar mutación a los candidatos
    mutated_generation = [mutate_individual(entry, p_ind, p_gen) for entry in mutated_candidates]

    return mutated_generation

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
