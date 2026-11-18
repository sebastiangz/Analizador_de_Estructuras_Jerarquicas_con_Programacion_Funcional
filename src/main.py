
"""
Archivo principal de OrganiTree.
Conecta la lectura de datos, la construcción del árbol organizacional
y las funciones de análisis mediante un menú interactivo de consola.

Los efectos externos (lectura de teclado, impresión en pantalla)
se concentran en este módulo. La lógica de búsqueda y análisis
permanece en sus módulos correspondientes.
"""

import sys
import os

# ---------------------------------------------------------------------------
# Ajuste de ruta: permite ejecutar el programa desde la raíz del proyecto
# con «python src/main.py» o «python -m src.main» sin errores de importación.
# ---------------------------------------------------------------------------
_directorio_src = os.path.dirname(os.path.abspath(__file__))
_directorio_proyecto = os.path.dirname(_directorio_src)

if _directorio_src not in sys.path:
    sys.path.insert(0, _directorio_src)
if _directorio_proyecto not in sys.path:
    sys.path.insert(0, _directorio_proyecto)

from datos import (
    leer_empleados,
    preparar_empleados,
    validar_empleados,
)

from arbol import (
    ID,
    NOMBRE,
    GERENTE,
    ID_GERENTE,
    DEPARTAMENTO,
    PUESTO,
    ESTADO,
    ID_RAIZ,
    construir_arbol,
    contar_empleados,
    calcular_altura,
    preorden,
    postorden,
    es_hoja,
    fold,
    contar_nodos,
)

from analisis import (
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


# =====================================================================
#  Funciones de presentación
# =====================================================================

def _separador():
    """Imprime una línea separadora."""
    print("=" * 56)


def mostrar_menu():
    """Presenta las opciones disponibles del sistema."""
    _separador()
    print("             O R G A N I T R E E")
    print("  Analizador de estructuras jerárquicas")
    _separador()
    print()
    print("  1. Mostrar organigrama")
    print("  2. Buscar empleado por ID")
    print("  3. Buscar empleado por nombre")
    print("  4. Mostrar subordinados de un empleado")
    print("  5. Consultar estadísticas generales")
    print("  6. Filtrar empleados por departamento")
    print("  7. Mostrar gerentes con más subordinados")
    print("  8. Mostrar departamentos con más empleados")
    print("  9. Mostrar advertencias de relaciones jerárquicas")
    print("  0. Salir")
    print()


def _mostrar_empleado(empleado):
    """Imprime los datos de un empleado en formato legible."""
    print(f"  ID:           {empleado[ID]}")
    print(f"  Nombre:       {empleado[NOMBRE]}")
    print(f"  Gerente:      {empleado[GERENTE] if empleado[GERENTE] else '(sin registro)'}")
    print(f"  ID Gerente:   {empleado[ID_GERENTE] if empleado[ID_GERENTE] else '(sin registro)'}")
    print(f"  Departamento: {empleado[DEPARTAMENTO]}")
    print(f"  Puesto:       {empleado[PUESTO]}")
    print(f"  Estado:       {empleado[ESTADO]}")


def _mostrar_empleado_breve(empleado):
    """Imprime una línea resumida de un empleado."""
    print(f"  [{empleado[ID]}] {empleado[NOMBRE]} — {empleado[PUESTO]} ({empleado[DEPARTAMENTO]})")


def _mostrar_organigrama(nodo, nivel=0):
    """Muestra el árbol con indentación según el nivel jerárquico.

    La recursión recorre primero el nodo actual y después sus hijos,
    lo que coincide con un recorrido preorden visual.
    """
    empleado, hijos = nodo
    indentacion = "    " * nivel

    if empleado[ID] == ID_RAIZ:
        # La raíz artificial se muestra de forma especial.
        print(f"{indentacion}🏢 {empleado[NOMBRE]}")
    elif hijos:
        print(f"{indentacion}├── 👤 [{empleado[ID]}] {empleado[NOMBRE]} — {empleado[PUESTO]}")
    else:
        print(f"{indentacion}├── 📄 [{empleado[ID]}] {empleado[NOMBRE]} — {empleado[PUESTO]}")

    for hijo in hijos:
        _mostrar_organigrama(hijo, nivel + 1)


# =====================================================================
#  Funciones de cada opción del menú
# =====================================================================

def opcion_mostrar_organigrama(arbol):
    """Opción 1: muestra el organigrama completo con indentación."""
    print("\n--- Organigrama de la organización ---\n")
    _mostrar_organigrama(arbol)
    print()


def opcion_buscar_por_id(arbol):
    """Opción 2: busca un empleado por su identificador."""
    empleado_id = input("\n  Ingrese el EmpID del empleado: ").strip()

    if not empleado_id:
        print("  No se proporcionó un identificador.")
        return

    resultado = buscar_por_id(arbol, empleado_id)

    if resultado is None:
        print(f"\n  No se encontró un empleado con EmpID '{empleado_id}'.")
    else:
        print(f"\n  Empleado encontrado:\n")
        _mostrar_empleado(resultado)
    print()


def opcion_buscar_por_nombre(arbol):
    """Opción 3: busca empleados cuyo nombre contenga el texto indicado."""
    nombre = input("\n  Ingrese el nombre (o parte del nombre): ").strip()

    if not nombre:
        print("  No se proporcionó un nombre.")
        return

    resultados = buscar_por_nombre(arbol, nombre)

    if not resultados:
        print(f"\n  No se encontraron empleados con '{nombre}' en su nombre.")
    else:
        print(f"\n  Se encontraron {len(resultados)} resultado(s):\n")
        for empleado in resultados:
            _mostrar_empleado_breve(empleado)
    print()


def opcion_mostrar_subordinados(arbol):
    """Opción 4: muestra los subordinados directos y todos los de niveles inferiores."""
    empleado_id = input("\n  Ingrese el EmpID del empleado: ").strip()

    if not empleado_id:
        print("  No se proporcionó un identificador.")
        return

    empleado = buscar_por_id(arbol, empleado_id)

    if empleado is None:
        print(f"\n  No se encontró un empleado con EmpID '{empleado_id}'.")
        return

    print(f"\n  Subordinados de: {empleado[NOMBRE]}\n")

    directos = obtener_subordinados_directos(arbol, empleado_id)

    if not directos:
        print("  Este empleado no tiene subordinados directos.")
    else:
        print(f"  Subordinados directos ({len(directos)}):\n")
        for sub in directos:
            _mostrar_empleado_breve(sub)

    todos = obtener_todos_los_subordinados(arbol, empleado_id)

    if len(todos) > len(directos):
        print(f"\n  Total de subordinados (todos los niveles): {len(todos)}\n")
        for sub in todos:
            if sub not in directos:
                print(f"    ↳ [{sub[ID]}] {sub[NOMBRE]} — {sub[PUESTO]}")
    print()


def opcion_estadisticas(arbol):
    """Opción 5: muestra las estadísticas generales de la organización."""
    estadisticas = calcular_estadisticas_generales(arbol)

    # Conteo de hojas usando fold.
    hojas = fold(
        arbol,
        lambda _empleado: 1,
        lambda _empleado, cantidades: sum(cantidades),
    )

    # La raíz artificial no cuenta como hoja real.
    _, hijos_raiz = arbol
    if not hijos_raiz:
        hojas = 0

    print("\n--- Estadísticas generales ---\n")
    print(f"  Total de empleados:           {estadisticas['total_empleados']}")
    print(f"  Niveles jerárquicos:          {estadisticas['niveles']}")
    print(f"  Altura del árbol (con raíz):  {calcular_altura(arbol)}")
    print(f"  Total de nodos (con raíz):    {contar_nodos(arbol)}")
    print(f"  Empleados sin subordinados:   {hojas}")
    print()


def opcion_filtrar_departamento(arbol):
    """Opción 6: filtra empleados por departamento."""
    # Primero mostrar los departamentos disponibles.
    ranking = departamentos_con_mas_empleados(arbol)

    if not ranking:
        print("\n  No se encontraron departamentos.")
        return

    print("\n  Departamentos disponibles:\n")
    for departamento, cantidad in ranking:
        print(f"    • {departamento} ({cantidad} empleados)")

    departamento = input("\n  Ingrese el nombre del departamento: ").strip()

    if not departamento:
        print("  No se proporcionó un departamento.")
        return

    empleados = filtrar_por_departamento(arbol, departamento)

    if not empleados:
        print(f"\n  No se encontraron empleados en '{departamento}'.")
    else:
        print(f"\n  Empleados en '{departamento}' ({len(empleados)}):\n")
        for empleado in empleados:
            _mostrar_empleado_breve(empleado)
    print()


def opcion_gerentes_subordinados(arbol):
    """Opción 7: muestra los gerentes que superan un umbral de subordinados directos."""
    umbral_texto = input(
        "\n  Ingrese el umbral de subordinados directos (default: 3): "
    ).strip()

    if not umbral_texto:
        umbral = 3
    else:
        try:
            umbral = int(umbral_texto)
        except ValueError:
            print("  El valor ingresado no es un número válido.")
            return

    gerentes = gerentes_con_muchos_subordinados(arbol, umbral)

    if not gerentes:
        print(f"\n  No hay gerentes con más de {umbral} subordinados directos.")
    else:
        print(f"\n  Gerentes con más de {umbral} subordinados directos:\n")
        for empleado, cantidad in gerentes:
            print(f"  [{empleado[ID]}] {empleado[NOMBRE]} — {cantidad} subordinados directos")
    print()


def opcion_departamentos_ranking(arbol):
    """Opción 8: muestra los departamentos ordenados por cantidad de empleados."""
    ranking = departamentos_con_mas_empleados(arbol)

    if not ranking:
        print("\n  No se encontraron departamentos.")
        return

    print("\n--- Departamentos con más empleados ---\n")

    posicion = 1
    for departamento, cantidad in ranking:
        print(f"  {posicion}. {departamento}: {cantidad} empleado(s)")
        posicion += 1
    print()


def opcion_advertencias(advertencias):
    """Opción 9: muestra las advertencias de relaciones jerárquicas."""
    if not advertencias:
        print("\n  No se registraron advertencias durante la construcción del árbol.")
    else:
        print(f"\n--- Advertencias ({len(advertencias)}) ---\n")
        for numero, advertencia in enumerate(advertencias, start=1):
            print(f"  {numero}. {advertencia}")
    print()


# =====================================================================
#  Función de ejecución de opciones
# =====================================================================

def ejecutar_opcion(opcion, arbol, advertencias):
    """Llama a la operación correspondiente según la opción seleccionada."""
    opciones = {
        "1": lambda: opcion_mostrar_organigrama(arbol),
        "2": lambda: opcion_buscar_por_id(arbol),
        "3": lambda: opcion_buscar_por_nombre(arbol),
        "4": lambda: opcion_mostrar_subordinados(arbol),
        "5": lambda: opcion_estadisticas(arbol),
        "6": lambda: opcion_filtrar_departamento(arbol),
        "7": lambda: opcion_gerentes_subordinados(arbol),
        "8": lambda: opcion_departamentos_ranking(arbol),
        "9": lambda: opcion_advertencias(advertencias),
    }

    funcion = opciones.get(opcion)

    if funcion is None:
        print("\n  Opción no válida. Intente de nuevo.")
    else:
        funcion()


# =====================================================================
#  Punto de entrada principal
# =====================================================================

def main():
    """Organiza la ejecución general del programa OrganiTree.

    1. Lee el archivo CSV.
    2. Prepara y valida los registros.
    3. Construye el árbol organizacional.
    4. Presenta el menú interactivo.
    """
    # Ruta del archivo CSV, relativa a la raíz del proyecto.
    ruta = os.path.join(_directorio_proyecto, "data", "HRDataset_v14.csv")

    print()
    _separador()
    print("  Cargando datos de empleados...")
    _separador()

    try:
        # 1. Leer los datos del archivo.
        registros = leer_empleados(ruta)

        # 2. Preparar los registros (seleccionar campos necesarios).
        empleados = preparar_empleados(registros)

        # 3. Validar los datos.
        errores = validar_empleados(empleados)

        if errores:
            print("\n  Se encontraron errores en los datos:\n")

            for error in errores:
                print(f"  ✗ {error}")

            print("\n  Corrija los errores en el archivo CSV e intente de nuevo.")
            return

        # 4. Construir el árbol organizacional.
        arbol, advertencias = construir_arbol(empleados)

        if arbol is None:
            print("\n  No fue posible construir el árbol:\n")

            for advertencia in advertencias:
                print(f"  ✗ {advertencia}")

            return

        # 5. Mostrar resumen de carga.
        total = contar_empleados(arbol)
        altura = calcular_altura(arbol)

        print(f"\n  ✓ Árbol organizacional construido correctamente.")
        print(f"    Empleados cargados: {total}")
        print(f"    Niveles jerárquicos: {max(0, altura - 1)}")

        if advertencias:
            print(f"    Advertencias: {len(advertencias)} (opción 9 para verlas)")

        print()

        # 6. Ciclo del menú interactivo.
        while True:
            mostrar_menu()

            opcion = input("  Seleccione una opción: ").strip()

            if opcion == "0":
                print("\n  ¡Hasta luego!\n")
                break

            ejecutar_opcion(opcion, arbol, advertencias)

            input("  Presione Enter para continuar...")

    except FileNotFoundError:
        print(f"\n  Error: no se encontró el archivo CSV en:")
        print(f"    {ruta}")
        print("  Asegúrese de que el archivo 'HRDataset_v14.csv' esté en la carpeta 'data/'.\n")

    except ValueError as error:
        print(f"\n  Error en el archivo: {error}\n")

    except KeyboardInterrupt:
        print("\n\n  Programa interrumpido por el usuario.\n")


if __name__ == "__main__":
    main()
