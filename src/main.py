
"""
Archivo principal de OrganiTree.
Conecta la lectura de datos con la construcción
del árbol organizacional.
"""

from datos import (
    leer_empleados,
    preparar_empleados,
    validar_empleados
)

from arbol import (
    construir_arbol,
    contar_empleados,
    calcular_altura
)


def main():
    # Ruta del archivo CSV.
    ruta = "data/HRDataset_v14.csv"

    try:
        # 1. Leer los datos del archivo.
        registros = leer_empleados(ruta)

        # 2. Preparar los registros.
        empleados = preparar_empleados(registros)

        # 3. Validar los datos.
        errores = validar_empleados(empleados)

        if errores:
            print("\nSe encontraron errores en los datos:")

            for error in errores:
                print("-", error)

            return

        # 4. Construir el árbol organizacional.
        arbol, advertencias = construir_arbol(empleados)

        if arbol is None:
            print("\nNo fue posible construir el árbol.")

            for advertencia in advertencias:
                print("-", advertencia)

            return

        # 5. Mostrar resultados.
        print("\n¡Árbol organizacional construido correctamente!")

        print("Total de empleados:", contar_empleados(arbol))
        print("Altura del árbol:", calcular_altura(arbol))

        if advertencias:
            print("\nAdvertencias:")

            for advertencia in advertencias:
                print("-", advertencia)

    except FileNotFoundError:
        print("Error: no se encontró el archivo CSV.")

    except ValueError as error:
        print("Error en el archivo:", error)


if __name__ == "__main__":
    main()
