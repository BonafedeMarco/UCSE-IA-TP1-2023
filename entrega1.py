from simpleai.search import SearchProblem
from simpleai.search.traditional import breadth_first, depth_first, limited_depth_first, iterative_limited_depth_first, \
    uniform_cost, greedy, astar
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer
import math

''' secuencia = jugar(
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
) '''

INITIAL_STATE = (("pieza_verde", 0, ((0, 0), (0, 1), (0, 2))),
                 ("pieza_roja", 0, ((1, 0), (2, 0))),
                 ("pieza_azul", 2, ((1, 0), (1, 1), (2, 1)))
)

PISOS = 2
FILAS = 5
COLUMNAS = 5
SALIDA = (0, 3, 1)
PIEZA_SACAR = "pieza_roja"

class RushHourProblem(SearchProblem):

    def obtener_pieza_objetivo(self, state):
        return list([pieza for pieza in state if pieza[0] == PIEZA_SACAR][0])

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
            distancias = []
            distancias.append(abs(piso - piso_salida))
            distancias.append(abs(fila - fila_salida))
            distancias.append(abs(col - col_salida))
            movimientos_por_parte.append(sum(distancias))

        return min(movimientos_por_parte)

    def result(self, state, action):
        return state


def jugar(self, filas, columnas, pisos, salida, piezas, pieza_sacar):
    return

if __name__ == '__main__':
    main()
