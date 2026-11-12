"""Módulo de análisis y consultas para el árbol organizacional de OrganiTree.

Contiene funciones puras para buscar empleados, filtrar registros y calcular
estadísticas básicas sobre la estructura jerárquica, aplicando principios de
programación funcional (inmutabilidad y funciones de orden superior).
"""

from typing import Callable
from src.arbol import ID, NOMBRE, DEPARTAMENTO, preorden, contar_empleados, fold


def buscar_por_id(arbol: tuple, empleado_id: str) -> tuple | None:
    """Busca y devuelve el registro de un empleado utilizando su EmpID.

    Recorre el árbol completo mediante preorden para localizar la coincidencia exacta.
    Devuelve None si no se encuentra el identificador.
    """
    empleados = preorden(arbol)
    for empleado in empleados:
        if empleado[ID] == empleado_id:
            return empleado
    return None


def buscar_por_nombre(arbol: tuple, nombre_buscado: str) -> tuple[tuple, ...]:
    """Busca empleados cuyo nombre coincida parcialmente (búsqueda flexible).

    Utiliza filtrado funcional para encontrar todas las coincidencias.
    """
    empleados = preorden(arbol)
    nombre_lower = nombre_buscado.strip().lower()

    return tuple(
        empleado
        for empleado in empleados
        if nombre_lower in empleado[NOMBRE].lower()
    )


def obtener_subordinados_directos(arbol: tuple, empleado_id: str) -> tuple[tuple, ...]:
    """Obtiene los subordinados directos de un empleado dado su ID.

    Busca el nodo correspondiente en el árbol y extrae los datos de sus hijos directos.
    """
    def _encontrar_nodo(nodo: tuple) -> tuple | None:
        empleado, hijos = nodo
        if empleado[ID] == empleado_id:
            return nodo
        for hijo in hijos:
            resultado = _encontrar_nodo(hijo)
            if resultado is not None:
                return resultado
        return None

    nodo_encontrado = _encontrar_nodo(arbol)
    if nodo_encontrado is None:
        return ()

    _, hijos_directos = nodo_encontrado
    # Extrae únicamente los datos del empleado de cada nodo hijo
    return tuple(hijo[0] for hijo in hijos_directos)


def filtrar_por_departamento(arbol: tuple, departamento: str) -> tuple[tuple, ...]:
    """Filtra y devuelve todos los empleados que pertenecen a un departamento específico.

    Excluye la raíz artificial de la organización.
    """
    empleados = preorden(arbol)
    depto_buscado = departamento.strip().lower()

    # Filtra ignorando la raíz artificial (cuyo ID es "ORG")
    return tuple(
        empleado
        for empleado in empleados
        if empleado[ID] != "ORG" and empleado[DEPARTAMENTO].strip().lower() == depto_buscado
    )


def calcular_estadisticas_generales(arbol: tuple) -> dict:
    """Calcula estadísticas generales de la organización usando funciones del árbol."""
    total_empleados = contar_empleados(arbol)
    
    return {
        "total_empleados": total_empleados,
    }