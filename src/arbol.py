"""Operaciones para construir y analizar el árbol organizacional de OrganiTree.

Formato de entrada esperado en construir_arbol:
    Una lista de diccionarios con las claves originales del CSV:
    EmpID, Employee_Name, ManagerName, ManagerID, Department,
    Position y EmploymentStatus.

Formato de un empleado dentro del árbol:
    (id, nombre, gerente, id_gerente, departamento, puesto, estado)

Formato de un nodo:
    (empleado, (hijo_1, hijo_2, ...))

Tanto el registro interno como la colección de hijos son tuplas. Por eso, una vez construido, el árbol no se modifica directamente.
"""

import unicodedata
from typing import Callable


# Posiciones de los datos dentro de la tupla de cada empleado.
# Se usan constantes para no tener que recordar los números de cada campo.
ID = 0
NOMBRE = 1
GERENTE = 2
ID_GERENTE = 3
DEPARTAMENTO = 4
PUESTO = 5
ESTADO = 6

# Identificador reservado para la raíz artificial de la organización.
ID_RAIZ = "ORG"

# Un empleado se guarda como una tupla de siete textos.
Empleado = tuple[str, str, str, str, str, str, str]

# Un nodo contiene un empleado y una tupla de nodos hijos.
# La cadena "Nodo" permite hacer referencia a la estructura recursiva.
Nodo = tuple[Empleado, tuple["Nodo", ...]]


RAIZ: Empleado = (
    ID_RAIZ,
    "Organización Dental Magic",
    "",
    "",
    "Organización",
    "Raíz",
    "",
)


def _texto(valor: object) -> str:
    """Convierte un valor a texto y elimina espacios de los extremos."""
    if valor is None:
        return ""
    return str(valor).strip()


def normalizar_nombre(nombre: str) -> str:
    """Normaliza un nombre para comparar Employee_Name con ManagerName.

    - Elimina espacios sobrantes.
    - Convierte "Apellido, Nombre" en "Nombre Apellido".
    - Ignora diferencias entre mayúsculas y minúsculas.
    - Elimina marcas de acentos para facilitar la comparación.

    Ejemplo:
        "  López,  Ana " -> "ana lopez"
        "ANA LOPEZ"      -> "ana lopez"
    """
    nombre = _texto(nombre)
    nombre = " ".join(nombre.split())

    # En el CSV Employee_Name puede venir como "Apellido, Nombre".
    if "," in nombre:
        apellidos, nombres = nombre.split(",", 1)
        nombre = nombres.strip() + " " + apellidos.strip()

    # Separa los acentos de las letras y elimina solamente las marcas.
    nombre = unicodedata.normalize("NFD", nombre)
    nombre = "".join(
        caracter
        for caracter in nombre
        if unicodedata.category(caracter) != "Mn"
    )

    return " ".join(nombre.casefold().split())


def _preparar_empleado(registro: dict) -> Empleado:
    """Convierte un registro del CSV a la tupla inmutable del proyecto."""
    return (
        _texto(registro.get("EmpID")),
        _texto(registro.get("Employee_Name")),
        _texto(registro.get("ManagerName")),
        _texto(registro.get("ManagerID")),
        _texto(registro.get("Department")),
        _texto(registro.get("Position")),
        _texto(registro.get("EmploymentStatus")),
    )


def _validar_empleados(empleados: tuple[Empleado, ...]) -> tuple[str, ...]:
    """Revisa los datos indispensables antes de construir el árbol.

    Devuelve una tupla de errores. Una tupla vacía significa que los datos básicos permiten continuar.
    """
    errores = ()

    for numero, empleado in enumerate(empleados, start=1):
        if not empleado[ID]:
            errores += (f"Registro {numero}: falta EmpID.",)
        if not empleado[NOMBRE]:
            errores += (f"Registro {numero}: falta Employee_Name.",)
        if empleado[ID] == ID_RAIZ:
            errores += (
                f"Registro {numero}: EmpID '{ID_RAIZ}' está reservado para la raíz.",
            )

    # Los identificadores deben ser únicos para poder relacionar los nodos.
    identificadores = tuple(empleado[ID] for empleado in empleados)
    ya_reportados = ()

    for identificador in identificadores:
        if identificador and identificadores.count(identificador) > 1:
            if identificador not in ya_reportados:
                errores += (f"EmpID duplicado: {identificador}.",)
                ya_reportados += (identificador,)

    return errores


def _buscar_empleados_por_nombre(
    empleados: tuple[Empleado, ...], nombre: str
) -> tuple[Empleado, ...]:
    """Devuelve todos los empleados cuyo nombre normalizado coincide."""
    nombre_buscado = normalizar_nombre(nombre)

    return tuple(
        empleado
        for empleado in empleados
        if normalizar_nombre(empleado[NOMBRE]) == nombre_buscado
    )


def _construir_relaciones(
    empleados: tuple[Empleado, ...]
) -> tuple[tuple[tuple[str, str | None], ...], tuple[str, ...]]:
    """Relaciona cada empleado con el EmpID de su gerente, si se encuentra.

    El resultado contiene pares (EmpID, EmpID_del_gerente). Cuando el gerente está vacío, es externo o su nombre es ambiguo, el segundo valor es None.
    """
    relaciones = ()
    advertencias = ()

    for empleado in empleados:
        nombre_gerente = empleado[GERENTE]

        if not normalizar_nombre(nombre_gerente):
            relaciones += ((empleado[ID], None),)
            advertencias += (
                f"{empleado[NOMBRE]} (EmpID {empleado[ID]}): no tiene ManagerName; "
                "se colocará como rama principal.",
            )
            continue

        coincidencias = _buscar_empleados_por_nombre(empleados, nombre_gerente)

        if len(coincidencias) == 1:
            gerente = coincidencias[0]
            relaciones += ((empleado[ID], gerente[ID]),)
        elif len(coincidencias) == 0:
            relaciones += ((empleado[ID], None),)
            advertencias += (
                f"{empleado[NOMBRE]} (EmpID {empleado[ID]}): el gerente "
                f"'{nombre_gerente}' no aparece como empleado; se colocará "
                "como rama principal.",
            )
        else:
            relaciones += ((empleado[ID], None),)
            advertencias += (
                f"{empleado[NOMBRE]} (EmpID {empleado[ID]}): el gerente "
                f"'{nombre_gerente}' coincide con varios empleados; la relación "
                "es ambigua y se colocará como rama principal.",
            )

    return relaciones, advertencias


def _validar_manager_id(
    empleados: tuple[Empleado, ...]
) -> tuple[str, ...]:
    """Advierte si un mismo ManagerID aparece con distintos ManagerName.

    No compara ManagerID con EmpID. Solamente comprueba que, dentro de los
    registros, un mismo identificador de gerente no esté asociado a nombres
    de gerente diferentes.
    """
    advertencias = ()

    for empleado in empleados:
        id_gerente = empleado[ID_GERENTE]
        nombre_gerente = normalizar_nombre(empleado[GERENTE])

        if not id_gerente or not nombre_gerente:
            continue

        nombres_del_mismo_id = tuple(
            normalizar_nombre(otro[GERENTE])
            for otro in empleados
            if otro[ID_GERENTE] == id_gerente and otro[GERENTE]
        )

        if len(set(nombres_del_mismo_id)) > 1:
            mensaje = (
                f"ManagerID {id_gerente} aparece asociado con varios nombres "
                "de gerente. Se recomienda revisar esos registros."
            )
            if mensaje not in advertencias:
                advertencias += (mensaje,)

    return advertencias


def _obtener_gerente_id(
    relaciones: tuple[tuple[str, str | None], ...], empleado_id: str
) -> str | None:
    """Busca el EmpID del gerente asignado a un empleado."""
    for id_empleado, id_gerente in relaciones:
        if id_empleado == empleado_id:
            return id_gerente
    return None


def _hay_ciclo_desde(
    empleado_id: str,
    relaciones: tuple[tuple[str, str | None], ...],
    visitados: tuple[str, ...] = (),
) -> bool:
    """Comprueba recursivamente si una cadena de supervisión forma un ciclo."""
    if empleado_id in visitados:
        return True

    gerente_id = _obtener_gerente_id(relaciones, empleado_id)

    if gerente_id is None:
        return False

    return _hay_ciclo_desde(
        gerente_id,
        relaciones,
        visitados + (empleado_id,),
    )


def _construir_nodo(
    empleado: Empleado,
    empleados: tuple[Empleado, ...],
    relaciones: tuple[tuple[str, str | None], ...],
) -> Nodo:
    """Construye un nodo y sus hijos mediante recursión."""
    # Primero se encuentran los empleados cuyo gerente es el nodo actual.
    empleados_hijos = tuple(
        otro_empleado
        for otro_empleado in empleados
        if _obtener_gerente_id(relaciones, otro_empleado[ID]) == empleado[ID]
    )

    # Después se construye recursivamente cada hijo.
    hijos = tuple(
        _construir_nodo(hijo, empleados, relaciones)
        for hijo in empleados_hijos
    )

    return (empleado, hijos)


def construir_arbol(
    registros: list[dict] | tuple[dict, ...]
) -> tuple[Nodo | None, tuple[str, ...]]:
    """Construye el árbol organizacional a partir de registros del CSV.

    Parámetro:
        registros: lista o tupla de diccionarios. Cada diccionario debe tener
        los encabezados del CSV: EmpID, Employee_Name, ManagerName, ManagerID,
        Department, Position y EmploymentStatus.

    Devuelve:
        (arbol, advertencias). Si hay errores que impiden construir una
        estructura segura (por ejemplo, EmpID duplicados o ciclos), devuelve
        (None, errores).

    Los supervisores externos, vacíos o ambiguos se muestran como ramas
    principales debajo de la raíz artificial. No se inventan empleados.
    """
    empleados = tuple(_preparar_empleado(registro) for registro in registros)

    errores = _validar_empleados(empleados)
    if errores:
        return None, errores

    relaciones, advertencias = _construir_relaciones(empleados)
    advertencias += _validar_manager_id(empleados)

    # Un árbol no puede tener relaciones circulares.
    hay_ciclo = any(
        _hay_ciclo_desde(empleado[ID], relaciones)
        for empleado in empleados
    )

    if hay_ciclo:
        return None, advertencias + (
            "Se detectó un ciclo en las relaciones de supervisión. "
            "No se puede construir un árbol válido.",
        )

    # La raíz es artificial y sirve para reunir todas las ramas principales.
    empleados_principales = tuple(
        empleado
        for empleado in empleados
        if _obtener_gerente_id(relaciones, empleado[ID]) is None
    )

    hijos_raiz = tuple(
        _construir_nodo(empleado, empleados, relaciones)
        for empleado in empleados_principales
    )

    arbol = (RAIZ, hijos_raiz)
    return arbol, advertencias


def preorden(arbol: Nodo) -> tuple[Empleado, ...]:
    """Devuelve los empleados en recorrido preorden: nodo antes que hijos.

    Nota: incluye la raíz artificial "Organización Dental Magic".
    """
    empleado, hijos = arbol

    resultado_hijos = tuple(
        empleado_hijo
        for hijo in hijos
        for empleado_hijo in preorden(hijo)
    )

    return (empleado,) + resultado_hijos


def postorden(arbol: Nodo) -> tuple[Empleado, ...]:
    """Devuelve los empleados en recorrido postorden: hijos antes que nodo.

    Nota: incluye la raíz artificial "Organización Dental Magic".
    """
    empleado, hijos = arbol

    resultado_hijos = tuple(
        empleado_hijo
        for hijo in hijos
        for empleado_hijo in postorden(hijo)
    )

    return resultado_hijos + (empleado,)


def inorden(arbol: Nodo) -> tuple[Empleado, ...]:
    """Devuelve un recorrido inorden con una convención para árboles n-arios.

    Como un nodo organizacional puede tener más de dos hijos, no existe un
    único inorder universal. En este proyecto se define así:
    primero se recorre el primer hijo, después el nodo actual y finalmente
    los hijos restantes en su orden original.

    La raíz artificial también se incluye en el resultado.
    """
    empleado, hijos = arbol

    if not hijos:
        return (empleado,)

    primer_hijo = inorden(hijos[0])
    hijos_restantes = tuple(
        empleado_hijo
        for hijo in hijos[1:]
        for empleado_hijo in inorden(hijo)
    )

    return primer_hijo + (empleado,) + hijos_restantes


def calcular_altura(arbol: Nodo) -> int:
    """Calcula la altura en cantidad de nodos del camino más largo.

    La raíz artificial también cuenta como un nivel. Por eso, si la
    organización tiene una sola persona debajo de la raíz, la altura es 2.
    Un nodo sin hijos tiene altura 1.
    """
    _, hijos = arbol

    if not hijos:
        return 1

    alturas_hijos = tuple(calcular_altura(hijo) for hijo in hijos)
    return 1 + max(alturas_hijos)


def fold(
    arbol: tuple,
    funcion_hoja: Callable,
    funcion_rama: Callable,
):
    """Reduce un árbol a un único resultado, procesándolo desde las hojas.

    - funcion_hoja recibe el valor de un nodo sin hijos.
    - funcion_rama recibe el valor de un nodo con hijos y los resultados
      obtenidos al procesar esos hijos.

    Esta función es genérica: también puede utilizarse con árboles pequeños
    de números, como los que aparecen en las pruebas.
    """
    valor, hijos = arbol

    if not hijos:
        return funcion_hoja(valor)

    resultados_hijos = tuple(
        fold(hijo, funcion_hoja, funcion_rama)
        for hijo in hijos
    )

    return funcion_rama(valor, resultados_hijos)


def contar_nodos(arbol: Nodo) -> int:
    """Cuenta todos los nodos del árbol, incluida la raíz artificial."""
    return fold(
        arbol,
        lambda _empleado: 1,
        lambda _empleado, cantidades: 1 + sum(cantidades),
    )


def contar_empleados(arbol: Nodo) -> int:
    """Cuenta los empleados sin incluir la raíz artificial de la organización."""
    return contar_nodos(arbol) - 1


def es_hoja(arbol: Nodo) -> bool:
    """Indica si un nodo no tiene hijos mediante pattern matching sencillo."""
    _, hijos = arbol

    # En Python 3.11, match/case permite distinguir la tupla vacía.
    match hijos:
        case ():
            return True
        case _:
            return False


def mapear_arbol(arbol: tuple, funcion: Callable) -> tuple:
    """Aplica una función a cada valor y devuelve un árbol nuevo.

    El árbol original no se modifica. La función recibida debe producir el
    nuevo valor que se almacenará en cada nodo.
    """
    valor, hijos = arbol
    nuevo_valor = funcion(valor)
    nuevos_hijos = tuple(
        mapear_arbol(hijo, funcion)
        for hijo in hijos
    )

    return (nuevo_valor, nuevos_hijos)


def crear_zipper(arbol: tuple) -> tuple:
    """Crea un zipper cuyo foco inicial es la raíz del árbol.

    Un zipper guarda:
        (nodo_actual, contexto)

    Cada elemento del contexto guarda el valor del padre, sus hermanos
    anteriores y sus hermanos posteriores. Todas esas colecciones son tuplas.
    """
    return (arbol, ())


def bajar(zipper: tuple, indice: int = 0) -> tuple | None:
    """Mueve el foco hacia uno de los hijos del nodo actual.

    Devuelve None si el nodo no tiene hijos o el índice no existe.
    El índice comienza en cero.
    """
    foco, contexto = zipper
    valor, hijos = foco

    if indice < 0 or indice >= len(hijos):
        return None

    hermanos_izquierda = hijos[:indice]
    hermanos_derecha = hijos[indice + 1:]
    marco = (valor, hermanos_izquierda, hermanos_derecha)

    nuevo_contexto = (marco,) + contexto
    return (hijos[indice], nuevo_contexto)


def subir(zipper: tuple) -> tuple:
    """Regresa el foco al padre y reconstruye sus hijos sin mutarlos.

    Si el foco ya está en la raíz, devuelve el zipper sin cambios.
    """
    foco, contexto = zipper

    if not contexto:
        return zipper

    valor_padre, hermanos_izquierda, hermanos_derecha = contexto[0]
    resto_contexto = contexto[1:]

    nuevos_hijos = hermanos_izquierda + (foco,) + hermanos_derecha
    nuevo_padre = (valor_padre, nuevos_hijos)

    return (nuevo_padre, resto_contexto)


def modificar_foco(zipper: tuple, funcion: Callable) -> tuple:
    """Aplica una función al valor del nodo actual y devuelve otro zipper.

    La modificación es inmutable: crea un foco nuevo y conserva el contexto.
    El árbol original no se altera.
    """
    foco, contexto = zipper
    valor, hijos = foco
    nuevo_foco = (funcion(valor), hijos)

    return (nuevo_foco, contexto)


def volver_a_raiz(zipper: tuple) -> tuple:
    """Sube recursivamente hasta recuperar el árbol completo."""
    if not zipper[1]:
        return zipper

    return volver_a_raiz(subir(zipper))


def unfold(
    semilla,
    condicion: Callable,
    generar_hijos: Callable,
) -> tuple:
    """Genera un árbol a partir de una semilla y una regla para crear hijos.

    Si condicion(semilla) es False, la semilla se convierte en una hoja.
    Si es True, generar_hijos(semilla) debe devolver una colección de nuevas
    semillas que se convertirán recursivamente en hijos.

    Importante: la condición debe hacer que la generación termine. De lo
    contrario, la recursión podría continuar indefinidamente.
    """
    if not condicion(semilla):
        return (semilla, ())

    semillas_hijas = generar_hijos(semilla)
    hijos = tuple(
        unfold(hijo, condicion, generar_hijos)
        for hijo in semillas_hijas
    )

    return (semilla, hijos)
