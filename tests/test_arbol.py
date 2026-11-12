"""Pruebas del módulo arbol.py usando unittest."""

import unittest
from copy import deepcopy

from src.arbol import (
    ID,
    NOMBRE,
    construir_arbol,
    preorden,
    postorden,
    inorden,
    calcular_altura,
    contar_nodos,
    contar_empleados,
    normalizar_nombre,
    es_hoja,
    mapear_arbol,
    fold,
    unfold,
    crear_zipper,
    bajar,
    subir,
    modificar_foco,
    volver_a_raiz,
)


class PruebasArbol(unittest.TestCase):
    """Comprueba la construcción y las operaciones principales del árbol."""

    def setUp(self):
        # Datos pequeños inventados para probar la lógica sin usar el CSV real.
        # Los nombres de empleados usan "Apellido, Nombre", como el dataset.
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
                "ManagerID": "100",
                "Department": "IT",
                "Position": "Manager",
                "EmploymentStatus": "Active",
            },
            {
                "EmpID": "3",
                "Employee_Name": "García, Luis",
                "ManagerName": "Carlos Ruiz",
                "ManagerID": "200",
                "Department": "IT",
                "Position": "Programmer",
                "EmploymentStatus": "Active",
            },
            {
                "EmpID": "4",
                "Employee_Name": "Pérez, Sofía",
                "ManagerName": "Ana López",
                "ManagerID": "100",
                "Department": "HR",
                "Position": "Manager",
                "EmploymentStatus": "Active",
            },
        ]
        self.arbol, self.advertencias = construir_arbol(self.empleados)

    def test_normalizar_nombre_cambia_formato_apellido_coma_nombre(self):
        self.assertEqual(normalizar_nombre("López, Ana"), "ana lopez")

    def test_normalizar_nombre_ignora_mayusculas_espacios_y_acentos(self):
        self.assertEqual(normalizar_nombre("  ANA   LOPEZ "), "ana lopez")
        self.assertEqual(normalizar_nombre("Garcia"), "garcia")
        self.assertEqual(normalizar_nombre("García"), "garcia")

    def test_construir_arbol_devuelve_un_arbol(self):
        self.assertIsNotNone(self.arbol)
        self.assertIsInstance(self.advertencias, tuple)

    def test_empleados_quedan_bajo_su_gerente(self):
        registros = preorden(self.arbol)
        ids = tuple(empleado[ID] for empleado in registros)

        # Raíz, Ana, Carlos, Luis y Sofía.
        self.assertEqual(ids, ("ORG", "1", "2", "3", "4"))

    def test_preorden_visita_primero_la_raiz(self):
        nombres = tuple(empleado[NOMBRE] for empleado in preorden(self.arbol))
        self.assertEqual(nombres[0], "Organización Dental Magic")

    def test_postorden_visita_al_final_la_raiz(self):
        nombres = tuple(empleado[NOMBRE] for empleado in postorden(self.arbol))
        self.assertEqual(nombres[-1], "Organización Dental Magic")

    def test_inorden_usa_la_convencion_documentada_para_varios_hijos(self):
        arbol_pequeno = (1, ((2, ()), (3, ()), (4, ())))
        self.assertEqual(inorden(arbol_pequeno), (2, 1, 3, 4))

    def test_calcular_altura_cuenta_la_raiz_artificial(self):
        # Organización -> Ana -> Carlos -> Luis: cuatro nodos de altura.
        self.assertEqual(calcular_altura(self.arbol), 4)

    def test_contar_nodos_incluye_la_raiz(self):
        self.assertEqual(contar_nodos(self.arbol), 5)

    def test_contar_empleados_excluye_la_raiz(self):
        self.assertEqual(contar_empleados(self.arbol), 4)

    def test_genera_advertencia_para_gerente_externo(self):
        empleados = [
            {
                "EmpID": "10",
                "Employee_Name": "Pérez, Marta",
                "ManagerName": "Board of Directors",
                "ManagerID": "999",
                "Department": "Executive",
                "Position": "Director",
                "EmploymentStatus": "Active",
            }
        ]

        arbol, advertencias = construir_arbol(empleados)
        self.assertIsNotNone(arbol)
        self.assertTrue(any("no aparece como empleado" in aviso for aviso in advertencias))
        self.assertEqual(contar_empleados(arbol), 1)

    def test_detecta_identificador_duplicado(self):
        empleados = self.empleados + [dict(self.empleados[0])]
        arbol, errores = construir_arbol(empleados)

        self.assertIsNone(arbol)
        self.assertTrue(any("EmpID duplicado" in error for error in errores))

    def test_detecta_nombre_de_empleado_vacio(self):
        empleados = [dict(self.empleados[0])]
        empleados[0]["Employee_Name"] = ""
        arbol, errores = construir_arbol(empleados)

        self.assertIsNone(arbol)
        self.assertTrue(any("falta Employee_Name" in error for error in errores))

    def test_detecta_ciclo_de_supervision(self):
        empleados = [
            {
                "EmpID": "1",
                "Employee_Name": "Uno, Ana",
                "ManagerName": "Carlos Dos",
                "ManagerID": "2",
                "Department": "IT",
                "Position": "Manager",
                "EmploymentStatus": "Active",
            },
            {
                "EmpID": "2",
                "Employee_Name": "Dos, Carlos",
                "ManagerName": "Ana Uno",
                "ManagerID": "1",
                "Department": "IT",
                "Position": "Manager",
                "EmploymentStatus": "Active",
            },
        ]

        arbol, errores = construir_arbol(empleados)
        self.assertIsNone(arbol)
        self.assertTrue(any("ciclo" in error.lower() for error in errores))

    def test_detecta_manager_id_asociado_a_nombres_diferentes(self):
        empleados = [
            {
                "EmpID": "1",
                "Employee_Name": "López, Ana",
                "ManagerName": "Directorio A",
                "ManagerID": "900",
                "Department": "Executive",
                "Position": "Director",
                "EmploymentStatus": "Active",
            },
            {
                "EmpID": "2",
                "Employee_Name": "Ruiz, Carlos",
                "ManagerName": "Directorio B",
                "ManagerID": "900",
                "Department": "IT",
                "Position": "Manager",
                "EmploymentStatus": "Active",
            },
        ]

        arbol, advertencias = construir_arbol(empleados)
        self.assertIsNotNone(arbol)
        self.assertTrue(any("ManagerID 900" in aviso for aviso in advertencias))

    def test_construccion_no_modifica_registros_de_entrada(self):
        empleados_originales = deepcopy(self.empleados)
        construir_arbol(self.empleados)
        self.assertEqual(self.empleados, empleados_originales)

    def test_nombres_ambiguos_no_se_asignan_a_un_gerente_al_azar(self):
        empleados = [
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
                "Employee_Name": "López, Ana",
                "ManagerName": "",
                "ManagerID": "",
                "Department": "Executive",
                "Position": "Director",
                "EmploymentStatus": "Active",
            },
            {
                "EmpID": "3",
                "Employee_Name": "Rivera, Juan",
                "ManagerName": "Ana López",
                "ManagerID": "100",
                "Department": "IT",
                "Position": "Analyst",
                "EmploymentStatus": "Active",
            },
        ]

        arbol, advertencias = construir_arbol(empleados)
        self.assertIsNotNone(arbol)
        self.assertTrue(any("ambigua" in aviso for aviso in advertencias))
        self.assertEqual(contar_empleados(arbol), 3)

    def test_identifica_una_hoja(self):
        hoja = ("valor", ())
        self.assertTrue(es_hoja(hoja))

    def test_identifica_un_nodo_con_hijos(self):
        arbol_pequeno = ("raiz", (("hijo", ()),))
        self.assertFalse(es_hoja(arbol_pequeno))

    def test_mapear_arbol_devuelve_un_arbol_nuevo(self):
        arbol_original = (1, ((2, ()), (3, ())))
        arbol_nuevo = mapear_arbol(arbol_original, lambda numero: numero * 10)

        self.assertEqual(arbol_original, (1, ((2, ()), (3, ()))))
        self.assertEqual(arbol_nuevo, (10, ((20, ()), (30, ()))))
        self.assertIsNot(arbol_original, arbol_nuevo)

    def test_fold_suma_los_valores_de_un_arbol(self):
        arbol_numerico = (1, ((2, ()), (3, ())))

        resultado = fold(
            arbol_numerico,
            lambda valor: valor,
            lambda valor, resultados_hijos: valor + sum(resultados_hijos),
        )

        self.assertEqual(resultado, 6)

    def test_zipper_baja_a_un_hijo_y_subir_reconstruye_el_arbol(self):
        arbol_original = ("raiz", (("A", ()), ("B", ())))
        zipper = crear_zipper(arbol_original)

        zipper_hijo = bajar(zipper, 1)
        self.assertIsNotNone(zipper_hijo)
        self.assertEqual(zipper_hijo[0], ("B", ()))

        zipper_padre = subir(zipper_hijo)
        self.assertEqual(zipper_padre[0], arbol_original)
        self.assertEqual(zipper_padre[1], ())

    def test_zipper_devuelve_none_si_no_existe_el_hijo(self):
        zipper = crear_zipper(("raiz", ()))
        self.assertIsNone(bajar(zipper, 0))
        self.assertIsNone(bajar(zipper, -1))

    def test_zipper_modifica_el_foco_sin_alterar_arbol_original(self):
        arbol_original = ("raiz", (("hijo", ()),))
        zipper = crear_zipper(arbol_original)
        zipper_hijo = bajar(zipper, 0)
        zipper_modificado = modificar_foco(
            zipper_hijo,
            lambda valor: valor.upper(),
        )
        arbol_nuevo = volver_a_raiz(zipper_modificado)

        self.assertEqual(arbol_nuevo[0], ("raiz", (("HIJO", ()),)))
        self.assertEqual(arbol_original, ("raiz", (("hijo", ()),)))

    def test_volver_a_raiz_conserva_el_arbol_si_ya_esta_en_la_raiz(self):
        arbol = ("raiz", ())
        zipper = crear_zipper(arbol)
        self.assertEqual(volver_a_raiz(zipper), zipper)

    def test_unfold_genera_un_arbol_desde_una_semilla(self):
        arbol_generado = unfold(
            1,
            lambda numero: numero < 3,
            lambda numero: (numero + 1,),
        )

        self.assertEqual(arbol_generado, (1, ((2, ((3, ()),)),)))

    def test_entrada_vacia_devuelve_raiz_sin_empleados(self):
        arbol, advertencias = construir_arbol([])

        self.assertIsNotNone(arbol)
        self.assertEqual(contar_empleados(arbol), 0)


if __name__ == "__main__":
    unittest.main()
