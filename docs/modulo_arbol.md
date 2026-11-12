# Guía del módulo `arbol.py`

Esta guía explica la parte del proyecto asignada a Kevin Osvaldo Barajas Anaya: representar, construir y recorrer el árbol organizacional.

## 1. ¿Qué es un árbol?

Un árbol es una estructura donde los elementos se organizan en niveles. Cada elemento es un **nodo**. Un nodo puede tener un padre y varios hijos. El nodo que inicia la estructura se llama **raíz**; los nodos sin hijos se llaman **hojas**.

En OrganiTree:

- Un empleado es un nodo.
- El gerente de un empleado es su padre.
- Los empleados que le reportan son sus hijos.
- La raíz artificial `Organización Dental Magic` agrupa las ramas principales.

Ejemplo:

```text
Organización Dental Magic
└── Ana López
    ├── Carlos Ruiz
    │   └── Luis García
    └── Sofía Pérez
```

La raíz artificial no es una persona del CSV y no debe contarse como empleado.

## 2. ¿Cómo representamos un nodo?

El módulo utiliza tuplas:

```python
nodo = (empleado, hijos)
```

El empleado también es una tupla con siete datos:

```python
(emp_id, nombre, manager_name, manager_id,
 departamento, puesto, estado)
```

Los hijos son otra tupla que contiene nodos:

```python
nodo = (datos_empleado, (nodo_hijo_1, nodo_hijo_2))
```

Se eligen tuplas porque no permiten cambiar sus elementos después de crearlas. Esto ayuda a cumplir el principio de **inmutabilidad**. Para hacer una transformación no cambiamos el árbol existente: construimos otro árbol con los nuevos valores.

## 3. Contrato de entrada con `datos.py`

Para que los módulos puedan trabajar juntos, Arturo debe entregar a `construir_arbol` una lista de diccionarios con los encabezados originales del CSV. Por ejemplo:

```python
empleados = [
    {
        "EmpID": "1",
        "Employee_Name": "López, Ana",
        "ManagerName": "",
        "ManagerID": "",
        "Department": "Executive",
        "Position": "Director",
        "EmploymentStatus": "Active"
    }
]

arbol, advertencias = construir_arbol(empleados)
```

El módulo `arbol.py` convierte cada diccionario en una tupla antes de construir la estructura. No modifica los diccionarios que recibe.

**Importante:** los valores `EmpID` y `ManagerID` no son la misma clave. La relación de supervisión se localiza comparando `ManagerName` con `Employee_Name` después de normalizar los nombres. `ManagerID` se conserva como dato y se utiliza para advertir si un mismo identificador de gerente aparece asociado con nombres diferentes; no se compara directamente con `EmpID`.

## 4. Normalización de nombres

En el CSV, `Employee_Name` puede aparecer como `Apellido, Nombre`, mientras que `ManagerName` puede aparecer como `Nombre Apellido`.

Por eso, antes de comparar dos nombres, `normalizar_nombre`:

1. Elimina espacios al principio y al final.
2. Reduce varios espacios a uno.
3. Si encuentra una coma, cambia el orden de apellido y nombre.
4. Convierte el texto a minúsculas.
5. Elimina las marcas de acentos para facilitar la comparación.

Ejemplo:

```python
normalizar_nombre("López, Ana")  # "ana lopez"
normalizar_nombre("ANA LOPEZ")   # "ana lopez"
```

Así ambos formatos pueden compararse.

## 5. Construcción del árbol

La función principal es:

```python
arbol, advertencias = construir_arbol(empleados)
```

Su procedimiento es:

1. Recibe los registros preparados por `datos.py`.
2. Convierte los campos necesarios en tuplas.
3. Revisa que cada empleado tenga `EmpID` y nombre.
4. Detecta identificadores duplicados.
5. Busca al gerente de cada empleado mediante el nombre normalizado.
6. Si el gerente aparece una sola vez, relaciona al empleado debajo de ese gerente.
7. Si el gerente no aparece, está vacío o su nombre coincide con varias personas, conserva al empleado como rama principal y devuelve una advertencia.
8. Comprueba que las relaciones no formen ciclos.
9. Construye recursivamente los nodos y los hijos.
10. Devuelve la raíz artificial con todas las ramas.

La función devuelve dos valores:

- El árbol y una tupla de advertencias cuando puede construirse.
- `None` y una tupla de errores cuando hay un problema que impide construirlo de forma segura, por ejemplo, identificadores duplicados o ciclos.

`None` es una forma sencilla de representar que no se obtuvo un árbol válido. Es una idea relacionada con `Maybe`, sin implementar una abstracción adicional.

## 6. Recursión

La recursión ocurre cuando una función se llama a sí misma para resolver una parte más pequeña del mismo problema.

En `_construir_nodo`:

- Primero se buscan los empleados que dependen directamente del empleado actual.
- Después se llama otra vez a `_construir_nodo` para construir cada uno de esos hijos.
- El proceso termina cuando un empleado no tiene subordinados. Ese caso se convierte en una hoja.

La condición de terminación es importante: un nodo sin hijos no necesita seguir llamando a la función.

También se usa recursión en los recorridos, en el cálculo de altura y en `fold`.

## 7. Recorridos

### Preorden

Primero visita el nodo actual y después recorre sus hijos.

```text
Raíz
A
B
C
```

Sirve para mostrar el organigrama de arriba hacia abajo.

### Postorden

Primero recorre los hijos y después visita el nodo actual.

```text
B
C
A
Raíz
```

Puede ser útil cuando se necesita procesar primero las ramas inferiores y luego el gerente.

Las funciones devuelven tuplas con los registros de empleados y **incluyen la raíz artificial**. Para obtener únicamente empleados, se debe excluir el registro cuyo `EmpID` es `ORG`.

### Inorden

El proyecto también incluye `inorden`. Como el árbol organizacional puede tener varios hijos, se adopta una convención sencilla para este proyecto: recorrer el primer hijo, visitar el nodo actual y después recorrer los hijos restantes. No es una definición universal de inorder para cualquier árbol n-ario; se documenta para que todos los integrantes interpreten el resultado de la misma manera.

## 8. Altura y conteo

- `calcular_altura(arbol)` devuelve la cantidad de nodos que hay en el camino más largo desde la raíz hasta una hoja. Incluye la raíz artificial.
- `contar_nodos(arbol)` cuenta todos los nodos, incluida la raíz artificial.
- `contar_empleados(arbol)` resta la raíz artificial para devolver únicamente empleados.

Si hay una raíz artificial, un director y un empleado subordinado, la altura es 3.

## 9. Fold

`fold` permite reducir un árbol completo a un único resultado.

Recibe dos funciones:

- `funcion_hoja`: indica qué hacer cuando un nodo no tiene hijos.
- `funcion_rama`: indica cómo combinar el valor del nodo con los resultados de sus hijos.

Ejemplo con números:

```python
arbol = (1, ((2, ()), (3, ())))

resultado = fold(
    arbol,
    lambda valor: valor,
    lambda valor, resultados: valor + sum(resultados)
)

# resultado = 6
```

La función procesa primero las hojas y después combina sus resultados hacia la raíz. `contar_nodos` utiliza `fold` para contar la estructura.

## 10. Unfold

`unfold` hace el proceso contrario a `fold`: comienza con una semilla y genera un árbol siguiendo una regla.

Recibe:

- Una semilla inicial.
- Una condición que indica si se deben generar hijos.
- Una función que devuelve las nuevas semillas.

Ejemplo:

```python
arbol = unfold(
    1,
    lambda numero: numero < 3,
    lambda numero: (numero + 1,)
)
```

La condición debe hacer que el proceso termine. Si siempre devuelve `True` y la función generadora nunca deja de producir hijos, la recursión podría continuar indefinidamente.

## 11. Pattern matching

`es_hoja` utiliza `match/case` de Python 3.11 para distinguir una tupla de hijos vacía (`()`) de una tupla con elementos.

- `case ()`: el nodo no tiene hijos.
- `case _`: el nodo tiene uno o más hijos.

Es una demostración pequeña de reconocimiento de la forma de una estructura.

## 12. Transformación inmutable con map

`mapear_arbol` recibe un árbol y una función. Aplica la función al valor de cada nodo y devuelve un árbol nuevo.

Ejemplo:

```python
original = (1, ((2, ()), (3, ())))
nuevo = mapear_arbol(original, lambda numero: numero * 10)

# original sigue siendo (1, ((2, ()), (3, ())))
# nuevo es (10, ((20, ()), (30, ())))
```

No se modifica la estructura original. Este es el principio de una transformación inmutable.

## 13. Zipper funcional

Un zipper permite enfocarse en una parte del árbol y conservar la información necesaria para regresar al padre. En este módulo se representa con una tupla:

```python
zipper = (nodo_actual, contexto)
```

El contexto guarda, para cada nivel, el valor del padre, los hermanos que estaban antes del nodo enfocado y los hermanos que estaban después.

Funciones disponibles:

- `crear_zipper(arbol)`: comienza con el foco en la raíz.
- `bajar(zipper, indice)`: mueve el foco a un hijo. Si el hijo no existe, devuelve `None`.
- `subir(zipper)`: regresa al padre reconstruyendo sus hijos.
- `modificar_foco(zipper, funcion)`: crea un foco nuevo aplicando una función al valor actual.
- `volver_a_raiz(zipper)`: regresa recursivamente hasta la raíz.

Ejemplo pequeño:

```python
arbol = ("raiz", (("A", ()), ("B", ())))
zipper = crear_zipper(arbol)

zipper_hijo = bajar(zipper, 1)   # foco en B
zipper_raiz = subir(zipper_hijo) # regresa a la raíz
```

Las operaciones no modifican el árbol original; generan nuevas tuplas. Esta es una versión didáctica para practicar navegación funcional. No se presenta como una implementación optimizada para árboles enormes.

## 14. Funciones puras y efectos

Las funciones de este módulo no abren archivos, no solicitan información al usuario y no imprimen resultados. Reciben datos y devuelven valores.

Por ejemplo:

```python
altura = calcular_altura(arbol)
```

La función no cambia el árbol ni escribe en un archivo. Esto permite probarla con datos pequeños y repetir la operación con la misma entrada.

## 15. Pruebas

Las pruebas están en `tests/test_arbol.py`. Se ejecutan desde la carpeta principal del repositorio:

```bash
python -m unittest discover -s tests -v
```

Los casos incluyen:

- Normalización de nombres.
- Construcción de la jerarquía.
- Preorden, inorden y postorden.
- Altura y conteo.
- Navegación zipper: bajar, subir, modificar foco y volver a la raíz.
- Gerentes externos o no encontrados.
- Identificadores duplicados.
- Nombres faltantes.
- Ciclos de supervisión.
- Detección de hojas.
- Transformación inmutable.
- Fold y unfold.
- Archivo de datos vacío.

Los datos de prueba son ficticios y pequeños. No se requiere descargar el CSV de Kaggle para ejecutar estas pruebas.

## 16. Complejidad, límites y decisiones

Este módulo está diseñado para el dataset de práctica, que tiene un tamaño pequeño. Para priorizar claridad, algunas búsquedas recorren repetidamente la colección de empleados. Esto puede ser menos eficiente que utilizar diccionarios de índices, pero es suficiente para el volumen de la actividad y permite comprender mejor las operaciones.

El módulo construye un árbol, no un grafo general. Si el profesor solicita analizar grafos con ciclos o relaciones múltiples entre nodos, eso deberá desarrollarse como una ampliación aparte.

Los supervisores externos no se inventan como empleados. Se coloca al empleado debajo de la raíz artificial y se devuelve una advertencia para que el usuario sepa que no se encontró su gerente en el CSV.
