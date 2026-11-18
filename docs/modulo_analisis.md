# Guía del módulo `analisis.py`

Esta guía explica la parte del proyecto asignada al módulo `analisis.py` de OrganiTree: realizar búsquedas, consultar subordinados, filtrar empleados y obtener estadísticas de la organización Dental Magic.

## 1. ¿Qué es el análisis de datos?

El análisis de datos consiste en revisar, organizar y consultar información para obtener resultados útiles.

En OrganiTree, el análisis se realiza utilizando el árbol organizacional que construye el módulo `arbol.py`.

Esto permite consultar información de los empleados sin tener que recorrer manualmente el archivo CSV.

En este módulo:

- Se buscan empleados mediante su identificador.
- Se buscan empleados por su nombre.
- Se consultan los subordinados de cada empleado.
- Se filtra información por departamento.
- Se filtra información por estado laboral.
- Se identifican los empleados con muchos subordinados.
- Se obtiene un ranking de departamentos.
- Se calculan estadísticas generales de la organización.

## 2. Relación con el módulo `arbol.py`

El módulo `analisis.py` depende de `arbol.py`, ya que utiliza el árbol organizacional que este construye.

Para trabajar, recibe un árbol como argumento:

```python
arbol, advertencias = construir_arbol(empleados)
```

Posteriormente, el árbol se utiliza en las funciones de análisis:

```python
resultado = buscar_por_id(arbol, "2")
```

El módulo importa diferentes constantes y funciones de `arbol.py`:

```python
from src.arbol import (
    ID,
    NOMBRE,
    DEPARTAMENTO,
    ESTADO,
    ID_RAIZ,
    preorden,
    calcular_altura,
)
```

Estas constantes permiten acceder a los datos de cada empleado sin tener que recordar manualmente la posición de cada campo dentro de la tupla.

Por ejemplo:

- `ID`: identificador del empleado.
- `NOMBRE`: nombre del empleado.
- `DEPARTAMENTO`: departamento al que pertenece.
- `ESTADO`: estado laboral.
- `ID_RAIZ`: identificador de la raíz artificial.
- `preorden`: permite recorrer los empleados del árbol.
- `calcular_altura`: permite conocer la altura de la organización.

**Importante:** el árbol contiene una raíz artificial llamada `Organización Dental Magic`. Esta raíz no representa a un empleado real, por lo que las funciones de análisis la excluyen de los resultados.

## 3. Búsqueda de empleados por ID

La función `buscar_por_id` permite localizar a un empleado utilizando su identificador.

Recibe dos parámetros:

- El árbol organizacional.
- El identificador del empleado que se desea encontrar.

Código:

```python
def buscar_por_id(arbol: tuple, empleado_id: str) -> tuple | None:
    empleados = filter(
        lambda empleado: empleado[ID] == empleado_id,
        preorden(arbol),
    )

    return next(
        (empleado for empleado in empleados if empleado[ID] != ID_RAIZ),
        None,
    )
```

La función utiliza `preorden` para recorrer el árbol y `filter` para encontrar al empleado cuyo ID coincida con el solicitado.

También utiliza `next` para devolver el primer resultado encontrado.

Si el empleado no existe, devuelve `None`.

Ejemplo:

```python
empleado = buscar_por_id(arbol, "2")
```

Si el empleado existe, devuelve su información; de lo contrario, devuelve `None`.

## 4. Búsqueda de empleados por nombre

La función `buscar_por_nombre` permite localizar empleados utilizando una parte de su nombre.

A diferencia de la búsqueda por ID, esta función puede devolver varios resultados.

Código:

```python
def buscar_por_nombre(arbol: tuple, nombre: str) -> tuple[tuple, ...]:
    nombre_buscado = nombre.strip().lower()

    empleados = filter(
        lambda empleado: (
            empleado[ID] != ID_RAIZ
            and nombre_buscado in empleado[NOMBRE].lower()
        ),
        preorden(arbol),
    )

    return tuple(empleados)
```

Su funcionamiento consiste en:

1. Recibir el nombre o texto que se desea buscar.
2. Eliminar espacios innecesarios al principio y al final.
3. Convertir el texto a minúsculas.
4. Recorrer los empleados mediante `preorden`.
5. Utilizar `filter` para encontrar las coincidencias.
6. Devolver los resultados en una tupla.

Ejemplo:

```python
resultados = buscar_por_nombre(arbol, "Ana")
```

Esta búsqueda permite encontrar empleados cuyo nombre contenga el texto indicado.

## 5. Búsqueda de nodos y subordinados

Para consultar los subordinados de un empleado, el módulo utiliza una función auxiliar llamada `_buscar_nodo`.

Esta función busca el nodo completo dentro del árbol, incluyendo sus hijos.

Código:

```python
def _buscar_nodo(arbol: tuple, empleado_id: str) -> tuple | None:
    empleado, hijos = arbol

    if empleado[ID] == empleado_id:
        return arbol

    for hijo in hijos:
        resultado = _buscar_nodo(hijo, empleado_id)

        if resultado is not None:
            return resultado

    return None
```

La función utiliza **recursión**, ya que se llama a sí misma para revisar los hijos de cada nodo.

Si encuentra el identificador solicitado, devuelve el nodo completo. Si no lo encuentra, devuelve `None`.

### 5.1. Obtener subordinados directos

La función `obtener_subordinados_directos` permite consultar únicamente a los empleados que dependen directamente de un gerente.

Código:

```python
def obtener_subordinados_directos(
    arbol: tuple, empleado_id: str
) -> tuple[tuple, ...]:

    nodo = _buscar_nodo(arbol, empleado_id)

    if nodo is None:
        return ()

    _, hijos = nodo

    return tuple(map(lambda hijo: hijo[0], hijos))
```

Su funcionamiento consiste en:

1. Buscar el nodo del empleado.
2. Obtener sus hijos.
3. Utilizar `map` para recuperar la información de cada subordinado.
4. Devolver los resultados en una tupla.

Si el empleado no existe o no tiene subordinados, devuelve una tupla vacía.

### 5.2. Obtener todos los subordinados

La función `obtener_todos_los_subordinados` permite consultar tanto los subordinados directos como los que pertenecen a niveles inferiores.

Código:

```python
def obtener_todos_los_subordinados(
    arbol: tuple, empleado_id: str
) -> tuple[tuple, ...]:

    nodo = _buscar_nodo(arbol, empleado_id)

    if nodo is None:
        return ()

    _, hijos = nodo

    return tuple(
        empleado
        for hijo in hijos
        for empleado in (hijo[0],) + obtener_todos_los_subordinados(
            hijo, hijo[0][ID]
        )
    )
```

Esta función también utiliza recursión para recorrer los diferentes niveles de la organización.

La diferencia con la función anterior es que no se limita a los hijos directos, sino que continúa buscando subordinados dentro de cada una de las ramas.

Por ejemplo, si Ana López tiene como subordinados a Carlos Ruiz y Sofía Pérez, y Carlos tiene como subordinado a Luis García, la función devolverá a los tres empleados.

## 6. Filtrar empleados por departamento

La función `filtrar_por_departamento` permite obtener todos los empleados que pertenecen a un departamento específico.

Código:

```python
def filtrar_por_departamento(
    arbol: tuple, departamento: str
) -> tuple[tuple, ...]:

    departamento_buscado = departamento.strip().lower()

    empleados = filter(
        lambda empleado: (
            empleado[ID] != ID_RAIZ
            and empleado[DEPARTAMENTO].strip().lower() == departamento_buscado
        ),
        preorden(arbol),
    )

    return tuple(empleados)
```

La función recibe el árbol y el nombre del departamento.

Primero normaliza el texto para evitar diferencias por espacios o mayúsculas. Después utiliza `filter` para seleccionar únicamente los empleados que pertenecen al departamento solicitado.

Ejemplo:

```python
empleados_it = filtrar_por_departamento(arbol, "IT")
```

De esta manera se pueden consultar los empleados de departamentos como IT, HR o Executive.

## 7. Filtrar empleados por estado laboral

La función `filtrar_por_estado` permite consultar empleados dependiendo de su situación laboral.

Código:

```python
def filtrar_por_estado(arbol: tuple, estado: str) -> tuple[tuple, ...]:
    estado_buscado = estado.strip().lower()

    empleados = filter(
        lambda empleado: (
            empleado[ID] != ID_RAIZ
            and empleado[ESTADO].strip().lower() == estado_buscado
        ),
        preorden(arbol),
    )

    return tuple(empleados)
```

Su funcionamiento es similar al filtro por departamento.

Recibe el estado laboral que se desea consultar, normaliza el texto y utiliza `filter` para obtener los empleados que coincidan.

Ejemplo:

```python
empleados_activos = filtrar_por_estado(arbol, "Active")
```

Esto permite consultar empleados con estados como `Active` o `Terminated`, dependiendo de los valores presentes en el archivo de datos.

## 8. Identificar gerentes con muchos subordinados

La función `gerentes_con_muchos_subordinados` permite identificar a los empleados que tienen una cantidad de subordinados directos superior a un límite establecido.

Código:

```python
def gerentes_con_muchos_subordinados(
    arbol: tuple, umbral: int
) -> tuple[tuple[tuple, int], ...]:

    nodos = _obtener_nodos(arbol)

    resultados = filter(
        lambda nodo: nodo[0][ID] != ID_RAIZ and len(nodo[1]) > umbral,
        nodos,
    )

    return tuple(
        (nodo[0], len(nodo[1]))
        for nodo in resultados
    )
```

Para realizar este análisis utiliza una función auxiliar llamada `_obtener_nodos`, que reúne los nodos del árbol mediante recursión.

El parámetro `umbral` indica la cantidad mínima que se utiliza como referencia.

Por ejemplo:

```python
gerentes = gerentes_con_muchos_subordinados(arbol, 1)
```

Si un empleado tiene dos subordinados directos, aparecerá en los resultados porque supera el umbral de uno.

Cada resultado contiene dos elementos:

- La información del empleado.
- La cantidad de subordinados directos que tiene.

**Nota:** la implementación considera cualquier empleado que tenga hijos en el árbol, sin comprobar específicamente que su puesto sea de gerente.

## 9. Departamentos con más empleados

La función `departamentos_con_mas_empleados` permite conocer cuántos empleados pertenecen a cada departamento y ordenarlos de mayor a menor.

Código:

```python
def departamentos_con_mas_empleados(
    arbol: tuple
) -> tuple[tuple[str, int], ...]:

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

    return tuple(sorted(
        cantidades,
        key=lambda resultado: resultado[1],
        reverse=True
    ))
```

Su funcionamiento consiste en:

1. Recorrer el árbol y obtener los empleados.
2. Excluir la raíz artificial.
3. Identificar los departamentos existentes.
4. Contar cuántos empleados pertenecen a cada departamento.
5. Ordenar los resultados de mayor a menor cantidad.

Ejemplo:

```python
ranking = departamentos_con_mas_empleados(arbol)
```

El resultado tiene la siguiente estructura:

```python
(
    ("IT", 2),
    ("HR", 1),
    ("Executive", 1)
)
```

Este ejemplo representa una organización donde IT tiene dos empleados, mientras que HR y Executive tienen uno cada uno.

Cuando dos departamentos tienen la misma cantidad, se conserva su orden de aparición original.

## 10. Estadísticas generales de la organización

La función `calcular_estadisticas_generales` permite obtener información general sobre el tamaño y los niveles de la organización.

Código:

```python
def calcular_estadisticas_generales(arbol: tuple) -> dict:
    empleados = tuple(
        empleado
        for empleado in preorden(arbol)
        if empleado[ID] != ID_RAIZ
    )

    total_empleados = reduce(
        lambda total, _empleado: total + 1,
        empleados,
        0,
    )

    niveles = max(0, calcular_altura(arbol) - 1)

    return {
        "total_empleados": total_empleados,
        "niveles": niveles,
    }
```

Esta función utiliza dos operaciones importantes:

- `reduce`: permite acumular un resultado a partir de los elementos de una colección. En este caso, cuenta el total de empleados.
- `calcular_altura`: obtiene la altura del árbol para conocer los niveles de la organización.

Como la raíz artificial también cuenta como un nivel en el cálculo de altura, se resta uno para obtener los niveles correspondientes a los empleados.

Ejemplo:

```python
estadisticas = calcular_estadisticas_generales(arbol)
```

El resultado tiene la siguiente estructura:

```python
{
    "total_empleados": 4,
    "niveles": 3
}
```

En este ejemplo, la organización cuenta con cuatro empleados distribuidos en tres niveles.

## 11. Programación funcional utilizada

El módulo `analisis.py` utiliza diferentes conceptos de programación funcional para trabajar con la información del árbol.

### Filter

Permite seleccionar los elementos que cumplen una condición.

Se utiliza principalmente en las búsquedas y filtros de empleados.

```python
empleados = filter(
    lambda empleado: empleado[ID] == "2",
    preorden(arbol)
)
```

### Map

Permite transformar los elementos de una colección aplicando una función.

Se utiliza para obtener la información de los subordinados.

```python
resultado = map(lambda hijo: hijo[0], hijos)
```

### Reduce

Permite combinar los elementos de una colección para obtener un solo resultado.

Se utiliza para contar el total de empleados.

```python
total = reduce(
    lambda acumulado, empleado: acumulado + 1,
    empleados,
    0
)
```

### Lambda

Permite crear funciones pequeñas y anónimas que se utilizan como argumentos de otras funciones.

Por ejemplo:

```python
lambda empleado: empleado[ID] == "2"
```

Esta expresión comprueba si el identificador de un empleado es igual a dos.

### Recursión

Consiste en que una función se llame a sí misma para resolver un problema por partes.

Se utiliza para buscar nodos y recorrer los subordinados de los diferentes niveles de la organización.

## 12. Funciones puras e inmutabilidad

El módulo `analisis.py` trabaja siguiendo el principio de inmutabilidad.

Esto significa que las funciones reciben el árbol organizacional, consultan su información y devuelven resultados sin modificar la estructura original.

Por ejemplo:

```python
empleado = buscar_por_id(arbol, "2")
```

Esta operación únicamente consulta los datos del árbol.

Además, las funciones no se encargan de abrir archivos, solicitar información al usuario ni imprimir resultados. Su responsabilidad es recibir datos y devolver valores.

Esto facilita realizar pruebas y reutilizar las funciones en otras partes del proyecto.

## 13. Pruebas del módulo

Las pruebas del módulo se encuentran en el archivo:

```text
tests/test_analisis.py
```

Se utiliza la biblioteca `unittest` de Python para comprobar que las funciones trabajen correctamente.

Las pruebas utilizan datos ficticios y pequeños, por lo que no es necesario cargar el CSV original para ejecutarlas.

Entre los casos que se comprueban se encuentran:

- Búsqueda de empleados por ID existente e inexistente.
- Búsqueda de empleados por nombre.
- Búsqueda sin distinguir mayúsculas y minúsculas.
- Obtención de subordinados directos.
- Obtención de todos los subordinados.
- Filtrado por departamento.
- Filtrado por estado laboral.
- Identificación de empleados con muchos subordinados.
- Clasificación de departamentos por cantidad de empleados.
- Cálculo del total de empleados y niveles de la organización.

Para ejecutar las pruebas desde la carpeta principal del proyecto se utiliza:

```bash
python -m unittest discover -s tests -v
```

Este comando ejecuta los archivos de pruebas que se encuentran dentro de la carpeta `tests`.

## 14. Relación con el funcionamiento de OrganiTree

El módulo `analisis.py` complementa el trabajo realizado por `arbol.py`, ya que permite aprovechar la estructura organizacional para consultar y obtener información de los empleados.

Mientras que `arbol.py` se encarga de construir y representar la jerarquía de la organización, `analisis.py` utiliza esa estructura para realizar búsquedas, filtros y cálculos.

De esta manera, ambos módulos trabajan en conjunto para facilitar la consulta y el análisis de la información de Dental Magic.

## 15. Consideraciones y limitaciones

El módulo está diseñado para trabajar con el árbol organizacional generado por `arbol.py`.

Algunas consideraciones importantes son:

- Las búsquedas dependen de los datos que contiene el árbol.
- La raíz artificial no se considera un empleado.
- Las funciones de búsqueda y filtrado devuelven tuplas.
- Si no se encuentran resultados, las funciones de búsqueda y filtrado devuelven una tupla vacía, excepto `buscar_por_id`, que devuelve `None`.
- Los subordinados se obtienen siguiendo las relaciones establecidas durante la construcción del árbol.
- El análisis de gerentes se basa en la cantidad de hijos directos de cada nodo, no en el nombre de su puesto.
- Las estadísticas generales cuentan únicamente empleados reales y descuentan la raíz artificial al calcular los niveles.

El propósito de este módulo es facilitar el análisis de la organización mediante operaciones funcionales, manteniendo la estructura original del árbol sin modificarla.