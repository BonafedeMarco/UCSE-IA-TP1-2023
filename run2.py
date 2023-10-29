from entrega2 import armar_tablero

'''
# DEFAULT TEST CASE
filas = 5
columnas = 5
pisos = 3
salida = (0, 3, 1)
piezas = [
        ("pieza_verde", "L"),
        ("pieza_roja", "O"),
        ("pieza_azul", "T"),
        ("pieza_amarilla", "T"),
]
pieza_sacar = "pieza_roja"
'''

# CUSTOM TEST CASE
filas = 5
columnas = 5
pisos = 3
salida = (0, 3, 1)
piezas = [
    ("pieza_verde", "L"),
    ("pieza_roja", "T"),
    ("pieza_azul", "O"),
    ("pieza_violeta", "I"),
    ("pieza_rosada", "-"),
    ("pieza_marron", "Z"),
    ("pieza_amarilla", "."),
    ("pieza_celeste", "O"),
    ("pieza_naranja", "I"),
]
pieza_sacar = "pieza_roja"

tablero = armar_tablero(filas, columnas, pisos, salida, piezas, pieza_sacar)

print(tablero)
for pieza in tablero:
    print(pieza, tablero[pieza])
