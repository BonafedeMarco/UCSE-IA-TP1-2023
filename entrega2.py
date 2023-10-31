from itertools import combinations
from simpleai.search import (
    CspProblem,
    backtrack,
    min_conflicts,
    MOST_CONSTRAINED_VARIABLE,
    HIGHEST_DEGREE_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
)
from simpleai.search.csp import _find_conflicts



TIPOS_PIEZAS = {
    "L": [[1, 0],
          [1, 1]]
    ,
    "T": [[1, 1, 1],
          [0, 1, 0]]
    ,
    "O": [[1, 1],
          [1, 1]]
    ,
    "I": [[1],
          [1],
          [1]]
    ,
    "-": [[1, 1, 1]]
    ,
    "Z": [[1, 1, 0],
          [0, 1, 1]]
    ,
    ".": [[1]]
}


PIEZAS_TIPO = {}

PIEZAS = []

PISOS = 0
FILAS = 0
COLUMNAS = 0
PIEZA_SACAR = ""
CASILLERO_SALIDA = ()


def generar_dominios():
    '''
    Define los dominios de todas las piezas,
    teniendo en cuenta su forma para que no se
    salgan del tablero
    '''
    DOMINIOS = {}

    for pieza in PIEZAS_TIPO:
        matriz_pieza = TIPOS_PIEZAS[PIEZAS_TIPO[pieza]]
        dominio = []
        for piso in range(PISOS):
            for row in range(FILAS - len(matriz_pieza) + 1):
                for col in range(COLUMNAS - len(matriz_pieza[0]) + 1):
                    dominio.append((piso, row, col))

        DOMINIOS[pieza] = dominio

    return DOMINIOS



def generar_pieza(tipo, coordenada_inicio):
    '''
    Retorna una lista de coordenadas en par (fila, columna)
    en base a la esquina superior izquierda y la forma
    '''

    coordenadas = []

    matriz_pieza = TIPOS_PIEZAS[tipo]

    for mod_fila, fila in enumerate(matriz_pieza):
        for mod_col, col in enumerate(fila):
            if col == 1:
                coordenadas.append([coordenada_inicio[1] + mod_fila, coordenada_inicio[2] + mod_col])

    return coordenadas



def verificar_no_colision(variables, values):
    '''
    Verifica que los bloques de piezas
    en el mismo piso no colisionen
    entre sí.
    '''

    inicio_pieza_1, inicio_pieza_2 = values
    pieza_1, pieza_2 = variables

    tipo_pieza_1 = PIEZAS_TIPO[pieza_1]
    tipo_pieza_2 = PIEZAS_TIPO[pieza_2]

    if inicio_pieza_1[0] == inicio_pieza_2[0]:

        coordenadas_p1 = tuple(map(tuple, generar_pieza(tipo_pieza_1, inicio_pieza_1)))
        coordenadas_p2 = tuple(map(tuple, generar_pieza(tipo_pieza_2, inicio_pieza_2)))

        if (tipo_pieza_1  == ".") or (tipo_pieza_2 == "."):

            if (tipo_pieza_1  == ".") and (tipo_pieza_2  == "."):
                return coordenadas_p1 != coordenadas_p2

            if (tipo_pieza_1  == "."):
                return coordenadas_p1[0] not in coordenadas_p2

            if (tipo_pieza_2  == "."):
                return coordenadas_p2[0] not in coordenadas_p1


        if bool(set(coordenadas_p1) & set(coordenadas_p2)):
            return False

    return True



def verificar_salida_libre(variables, values):
    '''
    Verifica que ninguna bloque se ubique en
    el mismo casillero que la salida
    '''

    piso, fila, columna = values[0]
    piso_s, fila_s, columna_s = CASILLERO_SALIDA

    if piso == piso_s:
        coordenadas_pieza = tuple(map(tuple, generar_pieza(PIEZAS_TIPO[variables[0]], values[0])))

        if len(coordenadas_pieza) == 1:
            return coordenadas_pieza[0] != (fila_s, columna_s)

        if (fila_s, columna_s) in coordenadas_pieza:
            return False

    return True



def verificar_cantidad_piezas(variables, values):
    '''
    Verifica que haya al menos una pieza por piso
    '''

    lista_pisos = set(pieza[0] for pieza in values)
    return len(lista_pisos) == PISOS



def verificar_cantidad_piezas_pisos(variables, values):
    '''
    Verifica que ningún piso tenga más del
    doble de piezas que el que menos tiene
    '''

    piezas_por_piso = [0 for x in range(PISOS)]

    for pieza in values:
        piezas_por_piso[pieza[0]] += 1

    return min(piezas_por_piso) * 2 >= max(piezas_por_piso)



def verificar_cantidad_bloques_piso(variables, values):
    '''
    Verifica que la cantidad de casillas ocupadas por piso
    no exceda 2/3 de la cantidad total del mismo
    '''

    bloques_por_piso = [[] for x in range(PISOS)]

    for indice_pieza, pieza in enumerate(values):
        bloques_por_piso[pieza[0]].extend(generar_pieza(PIEZAS_TIPO[PIEZAS[indice_pieza]], pieza))

    for piso in bloques_por_piso:
        if len(piso) > ((FILAS * COLUMNAS) / 3) * 2:
            return False

    return True



def pieza_sacar_distinto_piso_salida(variables, values):
    '''
    Verifica que la pieza a sacar no este en el mismo
    piso que la salida
    '''

    return values[0][0] != CASILLERO_SALIDA[0]



def generar_restricciones():
    '''
    Agrega todas las restricciones a la lista
    dado que ejecutar el programa con el if name main
    o desde un archivo aparte no corre
    el codigo suelto
    '''
    restricciones = []

    # Colisiones entre piezas
    for pieza1, pieza2 in combinations(PIEZAS, 2):
        restricciones.append(((pieza1, pieza2), verificar_no_colision))

    # Ninguna pieza sobre la salida
    for pieza in PIEZAS:
        restricciones.append(([pieza], verificar_salida_libre))

    # Una pieza por piso como mínimo
    restricciones.append((PIEZAS, verificar_cantidad_piezas))

    # Piso con más del doble de piezas que el que menos tiene
    restricciones.append((PIEZAS, verificar_cantidad_piezas_pisos))

    # Cantidad de bloques / segmentos de piezas
    restricciones.append((PIEZAS, verificar_cantidad_bloques_piso))

    # Pieza a sacar en distinto piso a la salida
    restricciones.append(([PIEZA_SACAR], pieza_sacar_distinto_piso_salida))

    return restricciones



def armar_tablero(filas, columnas, pisos, salida, piezas, pieza_sacar):
    '''
    Funcion para correr el programa desde
    otro archivo
    '''

    global PISOS
    global FILAS
    global COLUMNAS
    global PIEZA_SACAR
    global CASILLERO_SALIDA
    global PIEZAS_TIPO
    global PIEZAS

    PISOS = pisos
    FILAS = filas
    COLUMNAS = columnas
    PIEZA_SACAR = pieza_sacar
    CASILLERO_SALIDA = salida
    PIEZAS_TIPO = dict(piezas)
    PIEZAS = [key for key in PIEZAS_TIPO]

    DOMINIOS = generar_dominios()

    restricciones = generar_restricciones()

    problema = CspProblem(PIEZAS, DOMINIOS, restricciones)
    #solucion = backtrack(problema, variable_heuristic=MOST_CONSTRAINED_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)
    solucion = min_conflicts(problema)

    return solucion



if __name__ == "__main__":

    PISOS = 3
    FILAS = 5
    COLUMNAS = 5
    PIEZA_SACAR = "pieza_roja"
    CASILLERO_SALIDA =  (0, 3, 1)
    PIEZAS_TIPO = {
            "pieza_verde": "L",
            "pieza_roja": "T",
            "pieza_azul": "O",
            "pieza_violeta": "I",
            "pieza_rosada": ".",
            "pieza_marron": "Z",
            "pieza_amarilla": ".",
            "pieza_celeste": "O",
            "pieza_naranja": "I",
            }
    PIEZAS = [key for key in PIEZAS_TIPO]

    generar_dominios()

    generar_restricciones()

    problema = CspProblem(PIEZAS, DOMINIOS, restricciones)
    #solucion = backtrack(problema, variable_heuristic=MOST_CONSTRAINED_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)
    solucion = min_conflicts(problema)

    print("Solucion:")
    print(solucion)
