# Variables
x = 10
y = "Hola"
print(x)
print(y)

# Listas/Arreglos
lista_1 = [0, 1, 2]
lista_2 = [0, 10.5, 'a', "Adios"]
print("Segundo elemento de la lista: {}".format(lista_2[1]))
#print(lista_1)
#print(lista_2)
lista_1.append(3)
lista_1.append(-10)
print(lista_1.index(-10))
print(lista_1[4])


# Conjunto
conjunto_1={1, 2, 5, 4, 4}
print(conjunto_1)
conjunto_1.add(0)
print(conjunto_1)

# Diccionario
dicc_1 = {"Nombre": "Josué", "Edad": 22}
a = dicc_1["Edad"]
b = dicc_1["Nombre"]
print(a)
print(b)

# Tupla
tup = (5, 10.5, "variable")
p, q, r = tup
print(r)

def func_1(var1:float=1, var2:float=1):
    var3 = var1 + var2
    print("Resultado de la función interno: {}".format(var3))
    return var3

a = func_1
b = a(5, 5)
print("Resultado de la función: {}".format(b))
print("La función: {}".format(a))

def suma_multiple(*sumandos):
    print(sumandos)
    suma = 0
    for sumando in sumandos:
        print("Sumando = {}".format(sumando))
        suma = suma + sumando
        print("Suma = {}".format(suma))
    print(sumando)
    return suma
#suma_multiple(1, 2, 0, 10, 40)

def edades(Juan=10, Pedro=20, **personas):
    dicc = {"Juan": Juan, "Pedro": Pedro}
    print(personas)
    for nombre, edad in personas.items():
        dicc[nombre] = edad
    print(dicc)

edades(Pedro=50, Jose=80, Ivan=23)

