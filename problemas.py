#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
problemas.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""

import busquedas
import math
import copy



# ------------------------------------------------------------
#  Desarrolla el modelo del Camión mágico
# ------------------------------------------------------------

class PbCamionMagico(busquedas.ProblemaBusqueda):
    """
    ---------------------------------------------------------------------------------
     Supongamos que quiero trasladarme desde la posición discreta $1$ hasta 
     la posicion discreta $N$ en una vía recta usando un camión mágico. 
    
     Puedo trasladarme de dos maneras:
      1. A pie, desde el punto $x$ hasta el punto $x + 1$ en un tiempo de 1 minuto.
      2. Usando un camión mágico, desde el punto $x$ hasta el punto $2x$ con un tiempo 
         de 2 minutos.

     Desarrollar la clase del modelo del camión mágico
    ----------------------------------------------------------------------------------
    
    """
    def __init__(self, N):
        if not isinstance(N, int):
            raise TypeError("N debe ser entero")
        if N < 1:
            raise ValueError("N debe ser >= 1")
        
        self.N = N
        self.s_0 = 1
        #raise NotImplementedError('Hay que hacerlo de tarea')

    def acciones(self, estado):
        acciones = []

        if estado + 1 <= self.N:
            acciones.append("caminar")
        
        if estado * 2 <= self.N:
            acciones.append("camión")
        
        return acciones
        #raise NotImplementedError('Hay que hacerlo de tarea')

    def sucesor(self, estado, accion):
        if accion == "caminar":
            return estado + 1, 1

        elif accion == "camión":
            return estado * 2, 2
        
        else: 
            raise ValueError("Acción inválida")
        #raise NotImplementedError('Hay que hacerlo de tarea')

    def terminal(self, estado):
        return estado == self.N
        #raise NotImplementedError('Hay que hacerlo de tarea')

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        return f"Posición {estado}"
        #raise NotImplementedError('Hay que hacerlo de tarea')
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE
    
    Dado que no debemos sobreestimar el costo mínimo real restante y
    nuestra heurística debe ser 0 <= h(N) <= h*(N) para toda N
    Para cualquier estado N, el costo restante h*(N) >= 0 dado que 
    los costos de las acciones son positivos
    Esta heuristica en escencia no ayuda ya que solo vuelve 
    f(n) = g(n) + h(n)
    en 
    f(n) = g(n)
    lo cual se convierte en dijkstra, porque no establece
    una guia hacia el objetivo, pero no miente por exceso, por lo que
    nunca sobreestima

    """
    return 0
    


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_camion_magico(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    Simplifiquemos el problema como si solo pudieramos duplicar la posición
    x en la que estamos
    x = estado actual
    N = meta
    x <= N
    Si solamente duplicaramos el estado actual podriamos aproximar sin pasarnos
    a la meta con esta fórmula: 2^k * x <= N
    donde k es el número de veces que duplicamos sin pasarnos
    entonces, para saber cuantas veces podemos duplicar despejamos a k
    2^k <= N/x => log2(2^k) <= log2(N/x) => k <= log2(N/x)
    Despues el valor de log2(N/x) lo redondeamos hacia abajo para no sobreestimar
    utilizamos el maximo entre 0 y lo que devuelva math.floor....., para asegurar
    que la heuristica no sea negativa

    """
    x = nodo.estado
    N = problema.N
    
    return 2 * max(0, math.floor(math.log2(N / x)))

# ------------------------------------------------------------
#  Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------

# ------------------------------------------------------------
#  Funciones de Soporte para Hashability (Inmutabilidad)
# ------------------------------------------------------------

def hacer_inmutable(estado_dict):
    """Convierte el diccionario del cubo en una tupla de tuplas (Hashable)."""
    if isinstance(estado_dict, tuple): 
        return estado_dict
    return tuple((cara, tuple(colores)) for cara, colores in sorted(estado_dict.items()))

def hacer_dict(estado_tuple):
    """Convierte la tupla inmutable de vuelta a diccionario para lógica interna."""
    if isinstance(estado_tuple, dict): 
        return estado_tuple
    return {cara: list(colores) for cara, colores in estado_tuple}

# ------------------------------------------------------------
#  Modelo del Cubo de Rubik
# ------------------------------------------------------------

class PbCuboRubik(busquedas.ProblemaBusqueda):
    def __init__(self, estado_inicial=None):
        if estado_inicial:
            self.estado_inicial = estado_inicial
        else:
            self.estado_inicial = {
                'A': ['Blanco'] * 9, 'F': ['Verde'] * 9, 'D': ['Rojo'] * 9,
                'T': ['Azul'] * 9, 'I': ['Naranja'] * 9, 'B': ['Amarillo'] * 9
            }
        self.movimientos = ['A', "A'", 'F', "F'", 'D', "D'", 'T', "T'", 'I', "I'", 'B', "B'"]

    def acciones(self, estado):
        return self.movimientos

    def _rotar_90_horario(self, cara):
        c = cara
        return [c[6], c[3], c[0], c[7], c[4], c[1], c[8], c[5], c[2]]
    
    def _rotar_90_antihorario(self, cara):
        c = cara
        return [c[2], c[5], c[8], c[1], c[4], c[7], c[0], c[3], c[6]]

    def sucesor(self, estado_raw, accion):
        """
        Calcula el nuevo estado y devuelve (nuevo_estado, costo).
        Costo es 1 por cada giro de cara.
        """
        estado = hacer_dict(estado_raw)
        nuevo_estado = copy.deepcopy(estado)
        cara_obj = accion[0]
        es_anti = "'" in accion

        # 1. Rotación de la cara seleccionada
        if es_anti:
            nuevo_estado[cara_obj] = self._rotar_90_antihorario(estado[cara_obj])
        else:
            nuevo_estado[cara_obj] = self._rotar_90_horario(estado[cara_obj])

        # 2. Intercambio de bordes adyacentes
        if cara_obj == 'A':
            if not es_anti:
                nuevo_estado['F'][0:3], nuevo_estado['I'][0:3], nuevo_estado['T'][0:3], nuevo_estado['D'][0:3] = \
                    estado['D'][0:3], estado['F'][0:3], estado['I'][0:3], estado['T'][0:3]
            else:
                nuevo_estado['F'][0:3], nuevo_estado['D'][0:3], nuevo_estado['T'][0:3], nuevo_estado['I'][0:3] = \
                    estado['I'][0:3], estado['F'][0:3], estado['D'][0:3], estado['T'][0:3]
        
        elif cara_obj == 'B':
            if not es_anti:
                nuevo_estado['F'][6:9], nuevo_estado['D'][6:9], nuevo_estado['T'][6:9], nuevo_estado['I'][6:9] = \
                    estado['I'][6:9], estado['F'][6:9], estado['D'][6:9], estado['T'][6:9]
            else:
                nuevo_estado['F'][6:9], nuevo_estado['I'][6:9], nuevo_estado['T'][6:9], nuevo_estado['D'][6:9] = \
                    estado['D'][6:9], estado['F'][6:9], estado['I'][6:9], estado['T'][6:9]

        elif cara_obj == 'F':
            if not es_anti:
                nuevo_estado['D'][0], nuevo_estado['D'][3], nuevo_estado['D'][6] = estado['A'][6], estado['A'][7], estado['A'][8]
                nuevo_estado['B'][2], nuevo_estado['B'][1], nuevo_estado['B'][0] = estado['D'][0], estado['D'][3], estado['D'][6]
                nuevo_estado['I'][8], nuevo_estado['I'][5], nuevo_estado['I'][2] = estado['B'][2], estado['B'][1], estado['B'][0]
                nuevo_estado['A'][6], nuevo_estado['A'][7], nuevo_estado['A'][8] = estado['I'][8], estado['I'][5], estado['I'][2]
            else:
                nuevo_estado['I'][8], nuevo_estado['I'][5], nuevo_estado['I'][2] = estado['A'][6], estado['A'][7], estado['A'][8]
                nuevo_estado['B'][2], nuevo_estado['B'][1], nuevo_estado['B'][0] = estado['I'][8], estado['I'][5], estado['I'][2]
                nuevo_estado['D'][0], nuevo_estado['D'][3], nuevo_estado['D'][6] = estado['B'][2], estado['B'][1], estado['B'][0]
                nuevo_estado['A'][6], nuevo_estado['A'][7], nuevo_estado['A'][8] = estado['D'][0], estado['D'][3], estado['D'][6]

        elif cara_obj == 'D':
            idx, t_idx = [2, 5, 8], [6, 3, 0]
            for i in range(3):
                if not es_anti:
                    nuevo_estado['A'][idx[i]], nuevo_estado['F'][idx[i]], nuevo_estado['B'][idx[i]], nuevo_estado['T'][t_idx[i]] = \
                        estado['F'][idx[i]], estado['B'][idx[i]], estado['T'][t_idx[i]], estado['A'][idx[i]]
                else:
                    nuevo_estado['A'][idx[i]], nuevo_estado['T'][t_idx[i]], nuevo_estado['B'][idx[i]], nuevo_estado['F'][idx[i]] = \
                        estado['T'][t_idx[i]], estado['B'][idx[i]], estado['F'][idx[i]], estado['A'][idx[i]]

        elif cara_obj == 'I':
            idx, t_idx = [0, 3, 6], [8, 5, 2]
            for i in range(3):
                if not es_anti:
                    nuevo_estado['A'][idx[i]], nuevo_estado['T'][t_idx[i]], nuevo_estado['B'][idx[i]], nuevo_estado['F'][idx[i]] = \
                        estado['T'][t_idx[i]], estado['B'][idx[i]], estado['F'][idx[i]], estado['A'][idx[i]]
                else:
                    nuevo_estado['A'][idx[i]], nuevo_estado['F'][idx[i]], nuevo_estado['B'][idx[i]], nuevo_estado['T'][t_idx[i]] = \
                        estado['F'][idx[i]], estado['B'][idx[i]], estado['T'][t_idx[i]], estado['A'][idx[i]]

        elif cara_obj == 'T':
            idx_A, idx_I, idx_B, idx_D = [0,1,2], [6,3,0], [8,7,6], [2,5,8]
            for a, i, b, d in zip(idx_A, idx_I, idx_B, idx_D):
                if not es_anti:
                    nuevo_estado['I'][i], nuevo_estado['B'][b], nuevo_estado['D'][d], nuevo_estado['A'][a] = \
                        estado['A'][a], estado['I'][i], estado['B'][b], estado['D'][d]
                else:
                    nuevo_estado['A'][a], nuevo_estado['D'][d], nuevo_estado['B'][b], nuevo_estado['I'][i] = \
                        estado['I'][i], estado['A'][a], estado['D'][d], estado['B'][b]

        # Mantener el formato de entrada para la salida
        resultado = hacer_inmutable(nuevo_estado) if isinstance(estado_raw, tuple) else nuevo_estado
        return resultado, 1

    def terminal(self, estado_raw):
        estado = hacer_dict(estado_raw)
        return all(len(set(cara)) == 1 for cara in estado.values())

    @staticmethod
    def bonito(estado_raw):
        estado = hacer_dict(estado_raw)
        def f(cara, n):
            idx = n * 3
            return " ".join([c[0].upper() for c in estado[cara][idx:idx+3]])
        r = ["\n" + "="*25]
        for i in range(3): r.append(f"       {f('A', i)}")
        r.append("-" * 25)
        for i in range(3): r.append(f"{f('I', i)} | {f('F', i)} | {f('D', i)} | {f('T', i)}")
        r.append("-" * 25)
        for i in range(3): r.append(f"       {f('B', i)}")
        r.append("="*25 + "\n")
        return "\n".join(r)

# ------------------------------------------------------------
#  Heurísticas
# ------------------------------------------------------------
"""
    Esta heurística es muy "gruesa". Solo detecta si una cara está 
    perfecta o no. Si a una cara le falta una pegatina o le faltan 
    las nueve, el valor es el mismo. Esto genera muchas "mesetas" 
    donde el algoritmo no sabe hacia dónde moverse.
"""

def h_1_problema_1(nodo):
    estado = hacer_dict(nodo.estado if hasattr(nodo, 'estado') else nodo)
    incompletas = sum(1 for col in estado.values() if len(set(col)) > 1)
    return incompletas / 5.0

"""
    Esta es mucho más "fina" o granular. Detecta cambios mínimos en cada 
    movimiento. Al dividir por 20 (el máximo de pegatinas que cambian en 
    un giro), se mantiene admisible pero ofrece una guía mucho más 
    detallada.
"""
def h_2_problema_1(nodo):
    estado = hacer_dict(nodo.estado if hasattr(nodo, 'estado') else nodo)
    incorrectas = sum(1 for col in estado.values() for c in col if c != col[4])
    return incorrectas / 20.0
"""
    Conforme el cubo se desordena más, la probabilidad de que las 6 caras 
    estén "sucias" es casi del 100%. En ese punto, $h_1$ se estanca en un 
    valor fijo, mientras que $h_2$ sigue creciendo y discriminando entre 
    estados mejores y peores.
    Por esto h2 domina sobre h1 cuando el número de movimientos crece, 
    sin embargo, si el número de movimientos es muy pequeño >= 3 es 
    mejor h1
"""
# ------------------------------------------------------------
#  Comparación y Main
# ------------------------------------------------------------

def compara_metodos(problema, pos_inicial, h1, h2):
    """
    Ejecuta A* y muestra resultados. 
    Ajustado para cuando la librería devuelve (Nodo, int).
    """
    s0 = hacer_inmutable(pos_inicial)
    
    sol1, num_visitados1 = busquedas.busqueda_A_estrella(problema, s0, h1)
    sol2, num_visitados2 = busquedas.busqueda_A_estrella(problema, s0, h2)
    
    print('-' * 60)
    print('Método'.center(15) + 'Costo'.center(20) + 'Nodos visitados'.center(20))
    print('-' * 60)
    
    try:
        c1 = sol1.costo
        c2 = sol2.costo
    except AttributeError:
        c1 = sol1.g
        c2 = sol2.g

    linea1 = f"A* con h1".center(15) + f"{c1}".center(20) + f"{num_visitados1}".center(20)
    linea2 = f"A* con h2".center(15) + f"{c2}".center(20) + f"{num_visitados2}".center(20)
    
    print(linea1)
    print(linea2)
    print('-' * 60 + '\n')

if __name__ == "__main__":
    prob = PbCuboRubik()
    
    # Mezcla 
    # sucesor devuelve (estado, costo)
    e1, _ = prob.sucesor(prob.estado_inicial, 'A')
    e2, _ = prob.sucesor(e1, 'F')
    e3, _ = prob.sucesor(e2, 'B')
    e4, _ = prob.sucesor(e3, 'F')
    e5, _ = prob.sucesor(e4, 'A')
    
    print("Estado inicial para la comparación (2 movimientos de mezcla):")
    print(prob.bonito(e5))
    
    compara_metodos(prob, e5, h_1_problema_1, h_2_problema_1)