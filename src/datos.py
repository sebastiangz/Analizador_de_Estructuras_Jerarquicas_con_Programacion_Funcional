
"""
Modulo para leer, preparar y validar los datos de empleados
del proyecto OrganiTree.
"""

import csv


# Campos que necesita el proyecto para construir el arbol.
CAMPOS = (
    "EmpID",
    "Employee_Name",
    "ManagerName",
    "ManagerID",
    "Department",
    "Position",
    "EmploymentStatus"
)


def leer_empleados(ruta):
    """
    Lee el archivo CSV y devuelve una lista de diccionarios.

    Cada diccionario representa un empleado y utiliza
    los encabezados originales del archivo.
    """
    with open(ruta, "r", encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo)

        if lector.fieldnames is None:
            raise ValueError("El archivo CSV está vacío.")

        # Revisar que existan todos los campos necesarios.
        campos_faltantes = tuple(
            campo for campo in CAMPOS
            if campo not in lector.fieldnames
        )

        if campos_faltantes:
            raise ValueError(
                "Faltan columnas en el CSV: "
                + ", ".join(campos_faltantes)
            )

        return list(lector)


def preparar_empleados(registros):
    """
    Selecciona los campos necesarios y prepara los registros
    sin modificar la lista original.
    """
    empleados = []

    for registro in registros:
        empleado = {
            campo: (
                registro.get(campo, "").strip()
                if registro.get(campo) is not None
                else ""
            )
            for campo in CAMPOS
        }

        empleados.append(empleado)

    return empleados


def validar_empleados(empleados):
    """
    Revisa que los empleados tengan identificador y nombre,
    y que no existan identificadores repetidos.

    Devuelve una tupla con los errores encontrados.
    Si está vacía, los datos básicos son válidos.
    """
    errores = ()

    if not empleados:
        return ("El archivo no contiene empleados.",)

    # Revisar identificadores y nombres faltantes.
    for numero, empleado in enumerate(empleados, start=1):

        if not empleado["EmpID"]:
            errores += (
                f"Registro {numero}: falta EmpID.",
            )

        if not empleado["Employee_Name"]:
            errores += (
                f"Registro {numero}: falta Employee_Name.",
            )

    # Revisar que los EmpID no estén repetidos.
    identificadores = tuple(
        empleado["EmpID"] for empleado in empleados
    )

    duplicados_reportados = ()

    for identificador in identificadores:

        if identificador and identificadores.count(identificador) > 1:

            if identificador not in duplicados_reportados:
                errores += (
                    f"EmpID duplicado: {identificador}.",
                )

                duplicados_reportados += (identificador,)

    return errores
