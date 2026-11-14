
"""Pruebas del módulo analisis.py usando unittest."""

import unittest

from src.arbol import construir_arbol
from src.analisis import (
    buscar_por_id,
    buscar_por_nombre,
    obtener_subordinados_directos,
    obtener_todos_los_subordinados,
    filtrar_por_departamento,
    filtrar_por_estado,
    gerentes_con_muchos_subordinados,
    departamentos_con_mas_empleados,
    calcular_estadisticas_generales,
)


class PruebasAnalisis(unittest.TestCase):
    """Comprueba las funciones de búsqueda y análisis de empleados."""

    def setUp(self):
        # Datos de prueba para construir un árbol organizacional.
        self.empleados = [
            {
                "EmpID": "1",
                "Employee_Name": "López, Ana",
                "ManagerName": "",
                "ManagerID": "",
                "Department": "Executive",
                "Position": "Director",
                "EmploymentStatus": "Active",
            },
            {
                "EmpID": "2",
                "Employee_Name": "Ruiz, Carlos",
                "ManagerName": "Ana López",
                "ManagerID": "1",
                "Department": "IT",
                "Position": "Manager",
                "EmploymentStatus": "Active",
            },
            {
                "EmpID": "3",
                "Employee_Name": "García, Luis",
                "ManagerName": "Carlos Ruiz",
                "ManagerID": "2",
                "Department": "IT",
                "Position": "Programmer",
                "EmploymentStatus": "Terminated",
            },
            {
                "EmpID": "4",
                "Employee_Name": "Pérez, Sofía",
                "ManagerName": "Ana López",
                "ManagerID": "1",
                "Department": "HR",
                "Position": "Manager",
                "EmploymentStatus": "Active",
            },
        ]

        self.arbol, advertencias = construir_arbol(self.empleados)

        self.assertIsNotNone(
            self.arbol,
            msg=f"No se pudo construir el árbol: {advertencias}"
        )

    def test_buscar_por_id_existente(self):
        empleado = buscar_por_id(self.arbol, "2")

        self.assertIsNotNone(empleado)
        self.assertEqual(empleado[0], "2")
        self.assertEqual(empleado[1], "Ruiz, Carlos")

    def test_buscar_por_id_inexistente(self):
        empleado = buscar_por_id(self.arbol, "999")

        self.assertIsNone(empleado)

    def test_buscar_por_nombre(self):
        resultados = buscar_por_nombre(self.arbol, "Ana")

        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0][1], "López, Ana")

    def test_buscar_por_nombre_ignora_mayusculas(self):
        resultados = buscar_por_nombre(self.arbol, "ana")

        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0][1], "López, Ana")

    def test_obtener_subordinados_directos(self):
        # Ana López tiene dos subordinados directos.
        subordinados = obtener_subordinados_directos(
            self.arbol, "1"
        )

        nombres = tuple(empleado[1] for empleado in subordinados)

        self.assertEqual(len(subordinados), 2)
        self.assertIn("Ruiz, Carlos", nombres)
        self.assertIn("Pérez, Sofía", nombres)

    def test_obtener_todos_los_subordinados(self):
        # Ana tiene tres subordinados contando los niveles inferiores.
        subordinados = obtener_todos_los_subordinados(
            self.arbol, "1"
        )

        nombres = tuple(empleado[1] for empleado in subordinados)

        self.assertEqual(len(subordinados), 3)
        self.assertIn("Ruiz, Carlos", nombres)
        self.assertIn("Pérez, Sofía", nombres)
        self.assertIn("García, Luis", nombres)

    def test_filtrar_por_departamento(self):
        empleados_it = filtrar_por_departamento(
            self.arbol, "IT"
        )

        self.assertEqual(len(empleados_it), 2)
        self.assertEqual(
            tuple(empleado[1] for empleado in empleados_it),
            ("Ruiz, Carlos", "García, Luis")
        )

    def test_filtrar_por_departamento_ignora_mayusculas(self):
        empleados_it = filtrar_por_departamento(
            self.arbol, "it"
        )

        self.assertEqual(len(empleados_it), 2)

    def test_filtrar_por_estado(self):
        terminados = filtrar_por_estado(
            self.arbol, "Terminated"
        )

        self.assertEqual(len(terminados), 1)
        self.assertEqual(terminados[0][1], "García, Luis")

    def test_gerentes_con_muchos_subordinados(self):
        # Ana tiene dos subordinados directos y supera el umbral de 1.
        gerentes = gerentes_con_muchos_subordinados(
            self.arbol, 1
        )

        self.assertEqual(len(gerentes), 1)
        self.assertEqual(gerentes[0][0][1], "López, Ana")
        self.assertEqual(gerentes[0][1], 2)

    def test_departamentos_con_mas_empleados(self):
        ranking = departamentos_con_mas_empleados(self.arbol)

        # IT tiene dos empleados y debe aparecer primero.
        self.assertEqual(ranking[0][0], "IT")
        self.assertEqual(ranking[0][1], 2)

    def test_calcular_estadisticas_generales(self):
        estadisticas = calcular_estadisticas_generales(
            self.arbol
        )

        self.assertEqual(estadisticas["total_empleados"], 4)
        self.assertEqual(estadisticas["niveles"], 3)


if __name__ == "__main__":
    unittest.main()
