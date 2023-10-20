from simpleai.search import SearchProblem
from simpleai.search.traditional import breadth_first, depth_first, limited_depth_first, iterative_limited_depth_first, \
    uniform_cost, greedy, astar
from simpleai.search.viewers import WebViewer, BaseViewer
import math

'''
secuencia = jugar(
    filas=5,
    columnas=5,
    pisos=3,
    salida=(0, 3, 1),  # piso 0, fila 3, columna 1
    piezas=[
        # una lista de piezas presentes en el tablero, cada una con un id,
        # el piso en el que está, y la lista de coordenadas de sus partes
        # (las coordenadas en formato (fila, columna)
        {"id": "pieza_verde", "piso": 0, "partes": [(0, 0), (0, 1), (0, 2)]},
        {"id": "pieza_roja", "piso": 0, "partes": [(1, 0), (2, 0)]},
        {"id": "pieza_azul", "piso": 2, "partes": [(1, 0), (1, 1), (2, 1)]},
        ...
    ],
    pieza_sacar="pieza_roja",
)
'''

INITIAL_STATE = (
        ("pieza_verde", 1, ((0, 0), (0, 1), (1, 1))),
        ("pieza_roja", 2, ((0, 0), (0, 1))),
        ("pieza_azul", 0, ((2, 2), (2, 3), (3, 2))),
        ("pieza_amarilla", 2, ((0, 2), (1, 2)))
)

PISOS = 3
FILAS = 4
COLUMNAS = 4
SALIDA = (0, 3, 3)
PIEZA_SACAR = "pieza_roja"


def obtener_pieza_objetivo(state, pieza_a_retornar=PIEZA_SACAR):
    return list([pieza for pieza in state if pieza[0] == pieza_a_retornar][0])


def obtener_piezas_mismo_piso(state, pieza_a_mover):
    return list([pieza for pieza in state if (pieza[1] == pieza_a_mover[1]) & (pieza[0] != pieza_a_mover[0])])


def es_movimiento_valido(state, pieza_a_mover):
    nombre_pieza, piso_pieza, posiciones_partes = pieza_a_mover

    piezas_mismo_piso = obtener_piezas_mismo_piso(state, pieza_a_mover)

    # Control de que no se vaya de los limites verticales
    if piso_pieza < 0 or piso_pieza >= PISOS:
        return False

    # Limites laterales
    for coordenada in posiciones_partes:
        if not (0 <= coordenada[0] < FILAS):
            return False

        if not (0 <= coordenada[1] < COLUMNAS):
            return False

    # Colisiones
    for pieza in piezas_mismo_piso:
        if bool(set(pieza[2]) & set(posiciones_partes)):
            return False

    return True


def calcular_nueva_posicion(pieza_a_mover, movimiento):
    nombre_pieza, piso_pieza, posiciones_partes = pieza_a_mover

    mod_fila = 0
    mod_columna = 0
    mod_piso = 0

    if movimiento == "arriba":
        mod_fila = -1

    if movimiento == "abajo":
        mod_fila = 1

    if movimiento == "derecha":
        mod_columna = 1

    if movimiento == "izquierda":
        mod_columna = -1

    if movimiento == "trepar":
        mod_piso = 1

    if movimiento == "caer":
        mod_piso = -1

    piso_pieza += mod_piso

    lista_coordenadas = list(map(list, posiciones_partes))

    for coordenada in lista_coordenadas:
        coordenada[0] += mod_fila
        coordenada[1] += mod_columna

    return nombre_pieza, piso_pieza, tuple(map(tuple, lista_coordenadas))


class RushHourProblem(SearchProblem):

    def is_goal(self, state):
        nombre_pieza, piso_pieza, posiciones_partes = obtener_pieza_objetivo(state)
        piso_salida, fila_salida, col_salida = SALIDA

        if piso_pieza == piso_salida:
            if (fila_salida, col_salida) in posiciones_partes:
                return True

        return False

    def cost(self, state1, action, state2):
        return 1

    def actions(self, state):
        acciones = []
        movimientos = ("caer", "trepar", "arriba", "abajo", "derecha", "izquierda")

        for pieza in state:
            nombre_pieza, piso_pieza, posiciones_partes = pieza

            for movimiento in movimientos:
                if es_movimiento_valido(state, calcular_nueva_posicion(pieza, movimiento)):
                    acciones.append((nombre_pieza, movimiento))

        return acciones

    def heuristic(self, state):
        '''
        Distancia de Manhattan en 3D aplicada a cada una de las partes
        de la pieza a sacar con respecto a la salida. Se retorna el menor
        valor obtenido como cantidad mínima de movimientos suponiendo
        un tablero vacío.
        '''
        nombre_pieza, piso_pieza, posiciones_partes = obtener_pieza_objetivo(state)
        piso_salida, fila_salida, col_salida = SALIDA

        coordenadas_partes_absolutas = []

        for coordenada in posiciones_partes:
            coordenada = list(coordenada)
            coordenada.insert(0, piso_pieza)
            coordenadas_partes_absolutas.append(coordenada)

        movimientos_por_parte = []

        for parte in coordenadas_partes_absolutas:
            piso, fila, col = parte
            distancias = [abs(piso - piso_salida), abs(fila - fila_salida), abs(col - col_salida)]
            movimientos_por_parte.append(sum(distancias))

        return min(movimientos_por_parte)

    def result(self, state, action):
        nombre_pieza, piso_pieza, posiciones_partes = calcular_nueva_posicion(obtener_pieza_objetivo(state, action[0]), action[1])

        state = list(map(list, state))

        for pieza in state:
            if pieza[0] == nombre_pieza:
                pieza[1] = piso_pieza
                pieza[2] = list(map(list, pieza[2]))
                pieza[2] = posiciones_partes
                pieza[2] = tuple(map(tuple, pieza[2]))
                break

        return tuple(map(tuple, state))


def jugar(self, filas, columnas, pisos, salida, piezas, pieza_sacar):
    return


if __name__ == '__main__':
    my_problem = RushHourProblem(INITIAL_STATE)

   #v = WebViewer()

    result = astar(my_problem)# viewer=v)

    for action, state in result.path():
        print("A:", action)
        print("S:", state)
        print()
