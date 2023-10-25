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

piezas_uwu = {
    "pieza_verde": "L",
    "pieza_roja": "O",
    "pieza_azul": "T",
    "pieza_violeta": "T",
    "pieza_rosada": "T",
    "pieza_marron": "T",
    "pieza_amarilla": "T"
}

piezas = [
    "pieza_verde",
    "pieza_roja",
    "pieza_azul",
    "pieza_violeta",
    "pieza_rosada",
    "pieza_marron",
    "pieza_amarilla"
]

variables = piezas

PISO = 5
FILA = 5
COLUMNA = 5

dominios = {}

for pieza in piezas_uwu:
    matriz_pieza = tipos_piezas[piezas_uwu[pieza]]
    dominio = []
    for piso in range(PISO):
        for row in range(FILA - len(matriz_pieza[0]) + 1):
            for col in range(COLUMNA - len(matriz_pieza[1]) + 1):
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

        if bool(set(coordenada_p1) & set(coordenada_p2)):
            return False

    return True


# Verificar colision de piezas dentro de un piso
for pieza1, pieza2 in combinations(variables, 2):
    restricciones.append(
        ((pieza1, pieza2), verificar_no_colision)
    )

problema = CspProblem(variables, dominios, restricciones)
solucion = backtrack(problema, variable_heuristic=MOST_CONSTRAINED_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)

print("Solución:")
print(solucion)

# print(_find_conflicts(problema, solucion))
