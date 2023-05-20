'''import itertools

# Creamos un diccionario de conjuntos
dict_of_sets = {
    "A": {1, 2, 3},
    "B": {4, 5, 6},
    "C": {7, 8, 9}
}

# Unimos los conjuntos en un solo iterable usando itertools.chain
all_elements = itertools.chain(*dict_of_sets.values())

# Recorremos los elementos sin necesidad de un bucle for
while True:
    try:
        element = next(all_elements)
        print(element)
    except StopIteration:
        break'''
        
# Creamos un diccionario de conjuntos
'''dict_of_sets = {
    "A": {1, 2, 3},
    "B": {4, 5, 6},
    "C": {7, 8, 9}
}

# Recorremos el diccionario de conjuntos y sus elementos
for key, set_values in dict_of_sets.items():
    for element in set_values:
        print(f"La clave {key} contiene el elemento {element}")'''
 '''       
First = {
    "A" : {"ε","a"},
    "B" : {"b","ε"},
    "C" : {"c","ε"},
    "D" : {"d","ε"},
    "E" : {"e"},
    "S" : set([]),
    "a" : {"a"},
    "b" : {"b"},
    "c" : {"c"},
    "d" : {"d"},
    "e" : {"e"},
    "ε" : {"ε"}
} 

prodciones = {
    "A": ("a","ε"),
    "B": ("b","ε"),
    "C": ("c","ε"),
    "D": ("d","ε"),
    "E": ("e"),
    "S": ("ABCDE"),
}

note = ("A","B","C","D","E","S")
added = True   
while added:
    added = False
    for nt in note:
        for production in prodciones[nt]:
            for i in range(len(production)):
                first_sub_i = [First[j] for j in production[:i]]
                if i == 0:
                    first_sub_i.append({'ε'})
                if 'ε' in set.intersection(*first_sub_i):
                    First[nt].update(First[production[i]]-{'ε'})

                    
print(First["S"])'''


from collections import deque

stack = deque() # crea una pila vacía

# Agrega algunos elementos a la pila
stack.append(10)
stack.append(20)
stack.append(30)

# Obtén el primer elemento de la pila usando peek() o top()
primer_elemento = stack[-1] # También puedes usar stack.peek() o stack.top()

print(primer_elemento) # Imprime el primer elemento de la pila
