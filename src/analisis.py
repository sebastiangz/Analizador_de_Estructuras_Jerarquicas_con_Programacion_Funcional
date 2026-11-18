"""Funciones de búsqueda y análisis para OrganiTree

Este módulo recibe el árbol que construye arbol.py.
Las funciones no modifican el árbol original.
"""

from functools import reduce

try:
    from src.arbol import (
        ID,
        NOMBRE,
        DEPARTAMENTO,
        ESTADO,
        ID_RAIZ,
        preorden,
        calcular_altura,
    )
except ImportError:
    from arbol import (
        ID,
        NOMBRE,
        DEPARTAMENTO,
        ESTADO,
        ID_RAIZ,
        preorden,
        calcular_altura,
    )


def buscar_por_id(arbol: tuple, empleado_id: str) -> tuple | None:
    """Busca un empleado por su identificador."""
    empleados = filter(
        lambda empleado: empleado[ID] == empleado_id,
        preorden(arbol),
    )

    # La raíz artificial no es un empleado.
    return next(
        (empleado for empleado in empleados if empleado[ID] != ID_RAIZ),
        None,
    )


def buscar_por_nombre(arbol: tuple, nombre: str) -> tuple[tuple, ...]:
    """Busca empleados cuyo nombre contenga el texto indicado."""
    nombre_buscado = nombre.strip().lower()

    empleados = filter(
        lambda empleado: (
            empleado[ID] != ID_RAIZ
            and nombre_buscado in empleado[NOMBRE].lower()
        ),
        preorden(arbol),
    )

    return tuple(empleados)


def _buscar_nodo(arbol: tuple, empleado_id: str) -> tuple | None:
    """Busca el nodo completo para poder consultar sus hijos."""
    empleado, hijos = arbol

    if empleado[ID] == empleado_id:
        return arbol

    for hijo in hijos:
        resultado = _buscar_nodo(hijo, empleado_id)
        if resultado is not None:
            return resultado

    return None


def obtener_subordinados_directos(
    arbol: tuple, empleado_id: str
) -> tuple[tuple, ...]:
    """Devuelve únicamente los subordinados directos de un empleado."""
    nodo = _buscar_nodo(arbol, empleado_id)

    if nodo is None:
        return ()

    _, hijos = nodo

    # map obtiene los datos del empleado de cada nodo hijo.
    return tuple(map(lambda hijo: hijo[0], hijos))


def obtener_todos_los_subordinados(
    arbol: tuple, empleado_id: str
) -> tuple[tuple, ...]:
    """Devuelve los subordinados directos y los de niveles inferiores."""
    nodo = _buscar_nodo(arbol, empleado_id)

    if nodo is None:
        return ()

    _, hijos = nodo

    return tuple(
        empleado
        for hijo in hijos
        for empleado in (hijo[0],) + obtener_todos_los_subordinados(hijo, hijo[0][ID])
    )


def filtrar_por_departamento(
    arbol: tuple, departamento: str
) -> tuple[tuple, ...]:
    """Devuelve los empleados que pertenecen al departamento indicado."""
    departamento_buscado = departamento.strip().lower()

    empleados = filter(
        lambda empleado: (
            empleado[ID] != ID_RAIZ
            and empleado[DEPARTAMENTO].strip().lower() == departamento_buscado
        ),
        preorden(arbol),
    )

    return tuple(empleados)


def filtrar_por_estado(arbol: tuple, estado: str) -> tuple[tuple, ...]:
    """Devuelve los empleados que tienen el estado laboral indicado."""
    estado_buscado = estado.strip().lower()

    empleados = filter(
        lambda empleado: (
            empleado[ID] != ID_RAIZ
            and empleado[ESTADO].strip().lower() == estado_buscado
        ),
        preorden(arbol),
    )

    return tuple(empleados)


def _obtener_nodos(arbol: tuple) -> tuple[tuple, ...]:
    """Reúne los nodos del árbol para analizar sus subordinados."""
    _, hijos = arbol

    return (arbol,) + tuple(
        nodo
        for hijo in hijos
        for nodo in _obtener_nodos(hijo)
    )


def gerentes_con_muchos_subordinados(
    arbol: tuple, umbral: int
) -> tuple[tuple[tuple, int], ...]:
    """Devuelve los gerentes que tienen más subordinados que el umbral."""
    nodos = _obtener_nodos(arbol)

    resultados = filter(
        lambda nodo: nodo[0][ID] != ID_RAIZ and len(nodo[1]) > umbral,
        nodos,
    )

    return tuple((nodo[0], len(nodo[1])) for nodo in resultados)


def departamentos_con_mas_empleados(arbol: tuple) -> tuple[tuple[str, int], ...]:
    """Cuenta los empleados de cada departamento y ordena de mayor a menor."""
    empleados = tuple(
        empleado
        for empleado in preorden(arbol)
        if empleado[ID] != ID_RAIZ
    )

    departamentos = tuple(dict.fromkeys(
        empleado[DEPARTAMENTO]
        for empleado in empleados
        if empleado[DEPARTAMENTO]
    ))

    cantidades = map(
        lambda departamento: (
            departamento,
            len(tuple(filter(
                lambda empleado: empleado[DEPARTAMENTO] == departamento,
                empleados,
            ))),
        ),
        departamentos,
    )

    return tuple(sorted(cantidades, key=lambda resultado: resultado[1], reverse=True))


def calcular_estadisticas_generales(arbol: tuple) -> dict:
    """Calcula el total de empleados y los niveles de la organización."""
    empleados = tuple(
        empleado
        for empleado in preorden(arbol)
        if empleado[ID] != ID_RAIZ
    )

    # reduce acumula uno por cada empleado para obtener el total.
    total_empleados = reduce(
        lambda total, _empleado: total + 1,
        empleados,
        0,
    )

    # La altura de arbol.py cuenta la raíz artificial como un nivel.
    niveles = max(0, calcular_altura(arbol) - 1)

    return {
        "total_empleados": total_empleados,
        "niveles": niveles,
    }