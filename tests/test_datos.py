
"""Pruebas del módulo datos.py usando unittest."""

import unittest
import tempfile
import os
from copy import deepcopy

from src.datos import (
    leer_empleados,
    preparar_empleados,
    validar_empleados
)


class PruebasDatos(unittest.TestCase):
    """Comprueba la lectura, preparación y validación de empleados."""

    def setUp(self):
        # Datos pequeños inventados para realizar las pruebas.
        self.empleados = [
            {
                "EmpID": "1",
                "Employee_Name": "López, Ana",
                "ManagerName": "",
                "ManagerID": "",
                "Department": "Executive",
                "Position": "Director",
                "EmploymentStatus": "Active"
            },
            {
                "EmpID": "2",
                "Employee_Name": "Ruiz, Carlos",
                "ManagerName": "Ana López",
                "ManagerID": "100",
                "Department": "IT",
                "Position": "Manager",
                "EmploymentStatus": "Active"
            }
        ]

    def test_leer_empleados_lee_archivo_csv(self):
        # Crear un archivo CSV temporal para la prueba.
        contenido = (
            "EmpID,Employee_Name,ManagerName,ManagerID,"
            "Department,Position,EmploymentStatus\n"
            "1,López Ana,,,IT,Director,Active\n"
        )

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            suffix=".csv",
            delete=False
        ) as archivo:
            archivo.write(contenido)
            ruta = archivo.name

        try:
            registros = leer_empleados(ruta)

            self.assertEqual(len(registros), 1)
            self.assertEqual(registros[0]["EmpID"], "1")
            self.assertEqual(registros[0]["Department"], "IT")

        finally:
            os.remove(ruta)

    def test_preparar_empleados_selecciona_los_siete_campos(self):
        registros = preparar_empleados(self.empleados)

        self.assertEqual(len(registros), 2)
        self.assertEqual(
            tuple(registros[0].keys()),
            (
                "EmpID",
                "Employee_Name",
                "ManagerName",
                "ManagerID",
                "Department",
                "Position",
                "EmploymentStatus"
            )
        )

    def test_validar_empleados_detecta_campos_vacios(self):
        empleados = deepcopy(self.empleados)

        empleados[0]["Employee_Name"] = ""
        empleados[1]["EmpID"] = ""

        errores = validar_empleados(empleados)

        self.assertTrue(
            any("falta Employee_Name" in error for error in errores)
        )

        self.assertTrue(
            any("falta EmpID" in error for error in errores)
        )

    def test_validar_empleados_detecta_empid_duplicado(self):
        empleados = deepcopy(self.empleados)

        # Asignar el mismo identificador a dos empleados.
        empleados[1]["EmpID"] = "1"

        errores = validar_empleados(empleados)

        self.assertTrue(
            any("EmpID duplicado: 1" in error for error in errores)
        )

    def test_preparar_empleados_no_modifica_registros_originales(self):
        originales = deepcopy(self.empleados)

        preparar_empleados(self.empleados)

        self.assertEqual(self.empleados, originales)


if __name__ == "__main__":
    unittest.main()
