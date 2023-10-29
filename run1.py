from entrega1 import jugar


'''
filas=4
columnas=4
pisos=3
salida=(0, 3, 3)
piezas=[
    {"id": "pieza_verde", "piso": 1, "partes": [(0, 0), (0, 1), (1, 1)]},
    {"id": "pieza_roja", "piso": 2, "partes": [(0, 0), (0, 1)]},
    {"id": "pieza_azul", "piso": 0, "partes": [(2, 2), (2, 3), (3, 2)]},
    {"id": "pieza_amarilla", "piso": 2, "partes": [(0, 2), (1, 2)]},
]
pieza_sacar="pieza_roja"
'''

filas=4
columnas=4
pisos=6
salida=(0, 2, 1)
piezas=[
    {"id": "pieza_roja", "piso": 5, "partes": [(0, 1), (0, 2), (1, 2)]},
    {"id": "pieza_amarilla", "piso": 4, "partes": [(1, 1), (2, 1)]},
    {"id": "pieza_naranja", "piso": 3, "partes": [(0, 1), (1, 1), (1, 2), (2, 2)]},
    {"id": "pieza_azul", "piso": 1, "partes": [(0, 1), (1, 1), (2, 1), (3, 1)]},
    {"id": "pieza_celeste", "piso": 5, "partes": [(2, 1), (2, 2)]},
    {"id": "pieza_marron", "piso": 4, "partes": [(2, 2), (3, 2)]},
    {"id": "pieza_gris", "piso": 1, "partes": [(2, 3), (1, 3)]},
    {"id": "pieza_rosada", "piso": 4, "partes": [(0, 2), (0, 3), (1, 3)]},
    {"id": "pieza_verde", "piso": 0, "partes": [(1, 1), (1, 2), (2, 2)]},
    {"id": "pieza_violeta", "piso": 2, "partes": [(1, 1), (1, 2), (2, 2), (2, 1)]},
]
pieza_sacar="pieza_roja"

resultado = jugar(filas, columnas, pisos, salida, piezas, pieza_sacar)

for movimiento in resultado:
    print(movimiento)
