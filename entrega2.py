from itertools import combinations

from simpleai.search import (
    CspProblem,
    backtrack,
    min_conflicts,
    MOST_CONSTRAINED_VARIABLE,
    HIGHEST_DEGREE_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
    local
)

from simpleai.search.csp import _find_conflicts

tipos_piezas = {

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

PIEZA_SACAR = "pieza_roja"

CASILLERO_SALIDA = (0, 3, 1)

piezas_uwu = {
    "pieza_verde": "L",
    "pieza_roja": "T",
    "pieza_azul": "O",
    "pieza_violeta": "I",
    "pieza_rosada": "-",
    "pieza_marron": "Z",
    "pieza_amarilla": ".",
    "pieza_celeste": "O",
    "pieza_naranja": "I",
}

piezas = [
    "pieza_verde",
    "pieza_roja",
    "pieza_azul",
    "pieza_violeta",
    "pieza_rosada",
    "pieza_marron",
    "pieza_amarilla",
    "pieza_celeste",
    "pieza_naranja",
]

variables = piezas

PISO = 3
FILA = 5
COLUMNA = 5

dominios = {}

for pieza in piezas_uwu:
    matriz_pieza = tipos_piezas[piezas_uwu[pieza]]
    dominio = []
    for piso in range(PISO):
        for row in range(FILA - len(matriz_pieza) + 1):
            for col in range(COLUMNA - len(matriz_pieza[0]) + 1):
                dominio.append((piso, row, col))

    dominios[pieza] = dominio

restricciones = []


def generar_pieza(tipo, coordenada_inicio):
    coordenadas = []

    matriz_pieza = tipos_piezas[tipo]

    for mod_fila, fila in enumerate(matriz_pieza):
        for mod_col, col in enumerate(fila):
            if col == 1:
                coordenadas.append([coordenada_inicio[1] + mod_fila, coordenada_inicio[2] + mod_col])

    return coordenadas


def verificar_no_colision(variables, values):
    inicio_pieza_1, inicio_pieza_2 = values
    pieza_1, pieza_2 = variables

    if inicio_pieza_1[0] == inicio_pieza_2[0]:
        coordenada_p1 = tuple(map(tuple, generar_pieza(piezas_uwu[pieza_1], inicio_pieza_1)))
        coordenada_p2 = tuple(map(tuple, generar_pieza(piezas_uwu[pieza_2], inicio_pieza_2)))

        # Verifica colisiones

        if len(coordenada_p1) == 1 and len(coordenada_p2) == 1:
            return coordenada_p1 != coordenada_p2

        if len(coordenada_p1) == 1:
            return coordenada_p1 not in coordenada_p2

        if len(coordenada_p2) == 1:
            return coordenada_p2 not in coordenada_p1

        if bool(set(coordenada_p1) & set(coordenada_p2)):
            return False

    return True


# Verificar colision de piezas dentro de un piso
for pieza1, pieza2 in combinations(variables, 2):
    restricciones.append(
        ((pieza1, pieza2), verificar_no_colision)
    )


def verificar_salida_libre(variables, values):
    piso, fila, columna = values
    piso_s, fila_s, columna_s = CASILLERO_SALIDA

    if piso == piso_s:
        coordenada_pieza = tuple(map(tuple, generar_pieza(piezas_uwu[variables], values)))

        # Verifica colisiones

        if len(coordenada_pieza) == 1:
            return coordenada_pieza != (fila_s, columna_s)

        if (fila_s, columna_s) in coordenada_pieza:
            return False

    return True


for pieza in variables:
    restricciones.append((pieza, verificar_salida_libre))


def verificar_cantidad_piezas(variables, values):
    lista_pisos = set(pieza[0] for pieza in values)
    return len(lista_pisos) == PISO



restricciones.append((variables, verificar_cantidad_piezas))

def verificar_cantidad_piezas_pisos(variables, values):
    piezas_por_piso = [0 for x in range(PISO)]

    for pieza in values:
        piezas_por_piso[pieza[0]] += 1

    return min(piezas_por_piso) * 2 >= max(piezas_por_piso)


restricciones.append((variables, verificar_cantidad_piezas_pisos))


def verificar_cantidad_bloques_piso(variables, values):
    bloques_por_piso = [[] for x in range(PISO)]

    for indice_pieza, pieza in enumerate(values):
        bloques_por_piso[pieza[0]].extend(generar_pieza(piezas_uwu[variables[indice_pieza]], pieza))

    for piso in bloques_por_piso:
        if len(piso) > ((FILA * COLUMNA) / 4) * 3:
            return False

    return True


restricciones.append((variables, verificar_cantidad_bloques_piso))

def pieza_sacar_distinto_piso_salida(variables, values):
    return values[0] != CASILLERO_SALIDA[0]


restricciones.append((PIEZA_SACAR, pieza_sacar_distinto_piso_salida))

problema = CspProblem(variables, dominios, restricciones)
#solucion = backtrack(problema, variable_heuristic=MOST_CONSTRAINED_VARIABLE)
solucion = min_conflicts(problema)


print("Solución:")
print(solucion)

print(_find_conflicts(problema, solucion))
