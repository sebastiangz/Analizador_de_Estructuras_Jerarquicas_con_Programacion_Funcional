# OrganiTree

## Analizador de estructuras jerárquicas con programación funcional

Proyecto académico para la materia **Programación Funcional** de la **Ingeniería en Computación Inteligente, Universidad de Colima**.

> **Estado del proyecto:** planeación y organización inicial. Las funcionalidades descritas en este documento representan el alcance acordado; se marcarán como completadas conforme se implementen y prueben.

---

## 1. Descripción general

**OrganiTree** será un programa desarrollado en Python que permitirá leer información de empleados desde un archivo CSV, reconstruir sus relaciones de supervisión en forma de árbol y realizar consultas y análisis sobre esa estructura.

El sistema utilizará como fuente de prueba el conjunto de datos **Human Resources Data Set — Dental Magic**, publicado en Kaggle. El archivo contiene información de empleados de una empresa ficticia, incluidos sus nombres, puestos, departamentos y el nombre de sus gerentes.

A partir de esos datos, el programa construirá una representación jerárquica en la que:

- Cada empleado será representado como un nodo.
- Cada relación de supervisión será representada como una conexión entre un gerente y sus subordinados.
- Los empleados que supervisan a otros aparecerán como nodos con hijos.
- Los empleados sin subordinados aparecerán como hojas del árbol.
- Una raíz artificial llamada **Organización Dental Magic** permitirá reunir las ramas de la estructura. Esta raíz es únicamente un elemento de organización del programa; no representa a una persona ni un registro del CSV.

Una vez construida la estructura, el sistema permitirá buscar empleados, consultar subordinados, recorrer el árbol y calcular estadísticas. Las operaciones de análisis se desarrollarán aplicando principios de programación funcional, como recursión, inmutabilidad, funciones puras y funciones de orden superior.

## 2. Problema que busca resolver

En una organización, los datos de los empleados suelen estar almacenados en tablas o archivos. Aunque estos formatos permiten consultar registros individuales, no siempre muestran de manera directa cómo se relacionan las personas dentro de la estructura de supervisión.

Por ejemplo, a partir de una tabla de empleados puede ser difícil identificar rápidamente:

- Qué personas dependen directamente de un gerente.
- Cuántos niveles tiene una estructura organizacional.
- Qué gerentes tienen más subordinados directos.
- Qué departamentos concentran más empleados.
- Qué registros tienen un supervisor vacío o que no aparece entre los empleados.
- Qué relaciones jerárquicas necesitan revisarse por inconsistencias.

OrganiTree busca convertir los registros de empleados en una estructura jerárquica que facilite ese tipo de consultas y análisis.

## 3. Objetivo general

Desarrollar un sistema en Python que procese información de empleados y construya una estructura de árbol inmutable para analizar relaciones jerárquicas mediante funciones recursivas y operaciones propias de la programación funcional.

### 3.1 Objetivos específicos

1. Leer información de empleados desde un archivo CSV.
2. Seleccionar y preparar únicamente los campos necesarios para el análisis jerárquico.
3. Validar identificadores y relaciones de supervisión antes de construir el árbol.
4. Representar la organización mediante nodos y relaciones padre-hijo.
5. Implementar recorridos recursivos del árbol.
6. Desarrollar búsquedas por identificador y por nombre.
7. Calcular estadísticas como cantidad de empleados, subordinados directos, niveles y altura.
8. Aplicar `map`, `filter` y `reduce` en operaciones de procesamiento de información.
9. Mantener inmutable la estructura utilizada para los análisis y generar nuevas estructuras cuando se realicen transformaciones.
10. Comprobar el funcionamiento mediante pruebas y documentar las decisiones principales del proyecto.

---

## 4. Alcance del sistema

Para mantener el proyecto dentro de un nivel adecuado a los conocimientos actuales del equipo, se implementará primero un **analizador de árboles jerárquicos organizacionales**. No se pretende desarrollar una biblioteca general para procesar cualquier tipo de árbol, grafo, XML o JSON.

### 4.1 Funcionalidades contempladas

| Funcionalidad | Descripción |
|---|---|
| Lectura de datos | Leer los registros del CSV y extraer los campos necesarios. |
| Validación | Revisar identificadores duplicados, nombres de gerente faltantes y supervisores que no se puedan relacionar con un empleado. |
| Construcción del árbol | Relacionar a cada empleado con sus subordinados a partir de la información del gerente. |
| Visualización en consola | Mostrar el organigrama con indentación para distinguir los niveles. |
| Búsqueda | Localizar empleados por identificador o por nombre. |
| Consulta de subordinados | Obtener los subordinados directos de una persona y, cuando corresponda, los subordinados de niveles inferiores. |
| Recorridos | Recorrer el árbol en preorden y postorden. |
| Estadísticas | Calcular cantidad de empleados, cantidad de hojas, altura y subordinados directos. |
| Análisis por departamento | Filtrar y contar empleados según su departamento. |
| Análisis de gerentes | Identificar gerentes con un número elevado de subordinados directos, de acuerdo con un umbral configurable. |
| Transformaciones | Crear una nueva representación del árbol sin modificar la estructura original. |
| Pruebas | Comprobar las operaciones principales con ejemplos pequeños y controlados. |

### 4.2 Alcance mínimo y ampliaciones

El equipo priorizará que la lectura, construcción, búsqueda, recorridos y estadísticas funcionen correctamente antes de incorporar características adicionales.

**Alcance mínimo para tener un sistema funcional:**

- Leer el CSV.
- Validar los campos indispensables.
- Construir el árbol.
- Mostrar el árbol en consola.
- Buscar empleados.
- Obtener subordinados.
- Calcular estadísticas básicas.
- Demostrar recursión, inmutabilidad y uso de `map`, `filter` y `reduce`.
- Incluir pruebas y documentación.

**Ampliaciones sujetas al tiempo disponible o a indicaciones del profesor:**

- Una demostración sencilla de `unfold` para generar una estructura a partir de una semilla.
- Un recorrido por niveles (BFS).
- Una representación básica de grafo mediante listas de adyacencia para explicar la relación entre árboles y grafos.
- Una demostración reducida de zipper para navegar hacia un hijo y regresar al padre.
- Exportación o visualización gráfica del organigrama.

El proyecto original menciona grafos generales, `unfold`, pattern matching y zippers. Se reconoce su importancia, pero no se implementarán primero porque requieren conceptos adicionales. Para pattern matching se comenzará distinguiendo los casos del árbol de forma sencilla; `match/case` se incorporará solo si se confirma que el profesor lo espera como requisito explícito. El árbol organizacional sí puede entenderse como un caso particular de grafo dirigido: sus nodos son empleados y sus aristas representan relaciones de supervisión. Sin embargo, **un árbol no equivale a implementar todos los algoritmos de un grafo general**. Si el profesor exige algoritmos sobre grafos no jerárquicos, se añadirá como ampliación después de terminar el alcance mínimo.

---

## 5. Fuente de datos seleccionada

### 5.1 Human Resources Data Set — Dental Magic

- **Plataforma:** Kaggle.
- **Autores originales:** Dr. Rich Huebner y Dra. Carla Patalano.
- **Archivo de referencia:** `HRDataset_v14.csv`.
- **Tipo de archivo:** CSV.
- **Contenido:** registros de empleados de una organización ficticia llamada Dental Magic.
- **Enlace al dataset:** [Human Resources Data Set — Kaggle](https://www.kaggle.com/datasets/rhuebner/human-resources-data-set).
- **Diccionario de datos:** [HR Dataset v14 — Codebook](https://rpubs.com/rhuebner/hrd_cb_v14).

El conjunto fue creado con fines educativos para trabajar temas de recursos humanos, métricas y análisis. Sus registros son sintéticos; no deben interpretarse como datos reales de una empresa o de personas reales.

El codebook de los autores documenta 311 registros de empleados y 36 variables para su versión de referencia. Como pueden existir copias o versiones del archivo con columnas adicionales o pequeñas diferencias, el programa no debe depender de que el CSV tenga una cantidad fija de columnas. Debe localizar los campos por el nombre de su encabezado.

### 5.2 Campos que utilizará el proyecto

Aunque el dataset contiene más información, OrganiTree utilizará únicamente los campos necesarios para construir y analizar la estructura organizacional:

| Campo del CSV | Uso dentro del sistema |
|---|---|
| `Employee_Name` | Nombre del empleado. |
| `EmpID` | Identificador único del empleado. |
| `ManagerName` | Nombre del supervisor inmediato indicado para el empleado. |
| `ManagerID` | Identificador asignado al gerente en los registros del dataset; se utilizará como dato auxiliar de validación. |
| `Department` | Departamento al que pertenece el empleado. |
| `Position` | Puesto del empleado. |
| `EmploymentStatus` | Estado laboral registrado. |

No se utilizarán para el análisis jerárquico campos como salario, fecha de nacimiento, género, estado civil o datos demográficos. No aportan información necesaria para construir el árbol y se excluyen para mantener el proyecto enfocado en su objetivo.

### 5.3 Consideración importante: `EmpID` no es `ManagerID`

Estos campos **no representan el mismo tipo de identificador**:

- `EmpID` identifica a un empleado.
- `ManagerID` es un identificador asignado al gerente registrado en la fila.

Por lo tanto, no se debe intentar relacionar directamente `ManagerID` con `EmpID` como si fueran una misma clave.

La relación jerárquica se reconstruirá principalmente mediante `ManagerName` y `Employee_Name`. Antes de compararlos, será necesario normalizar los nombres, porque el dataset puede presentar formatos diferentes. Por ejemplo:

| Campo | Valor |
|---|---|
| `Employee_Name` | `King, Janet` |
| Nombre normalizado del empleado | `Janet King` |
| `ManagerName` de otros registros | `Janet King` |

La normalización deberá contemplar, como mínimo, espacios sobrantes y el formato `Apellido, Nombre` del campo `Employee_Name`. Si un nombre de gerente no puede asociarse con un empleado, el programa deberá reportarlo como supervisor externo o no identificado; no debe inventar un registro de empleado para completar la jerarquía.

El campo `ManagerID` podrá ayudar a comprobar que un mismo identificador de gerente no esté asociado a nombres diferentes, pero no sustituye la correspondencia entre el nombre del supervisor y el registro del empleado.

### 5.4 Raíces y relaciones no encontradas

Para mostrar una sola estructura, el programa utilizará una raíz artificial llamada `Organización Dental Magic`. Esta raíz no contará como empleado.

Cuando `ManagerName` corresponda a un empleado que aparece en el CSV, se colocará al empleado debajo de ese gerente. Cuando el gerente sea una referencia externa —por ejemplo, `Board of Directors`— o no pueda relacionarse con un registro de empleado, el empleado se mostrará como una rama principal y se conservará una advertencia que indique que su supervisor no aparece como empleado en el archivo.

Si el campo del gerente está vacío, el registro también deberá reportarse como una relación de supervisión no registrada. El sistema no debe confundir una relación desconocida con una relación inexistente.

Durante la construcción se revisará que:

- No existan `EmpID` duplicados.
- Los empleados tengan identificador y nombre.
- Los nombres de gerente se puedan normalizar y comparar.
- No se generen ciclos de supervisión.
- Los supervisores externos o no encontrados queden identificados en el resultado de validación.

### 5.5 Descarga y uso local

1. Entrar al enlace de Kaggle.
2. Iniciar sesión o crear una cuenta si Kaggle lo solicita.
3. Descargar el archivo CSV del dataset.
4. Identificar el archivo `HRDataset_v14.csv`.
5. Colocar el archivo localmente en la carpeta `data/` del proyecto.
6. Mantener el archivo original sin editar. La lectura, selección de columnas y construcción del árbol las realizará el programa.

**Importante sobre la licencia:** la ficha de Kaggle indica una licencia **CC BY-NC-ND 4.0**. Se deberá reconocer a los autores y la fuente, limitar el uso al contexto no comercial permitido por la licencia y no publicar una versión modificada del dataset.

El proyecto es académico. La propuesta de emprendimiento descrita más adelante es una idea de producto, no una autorización para comercializar el dataset ni sus derivados. Antes de cualquier uso comercial se tendría que revisar y obtener una fuente de datos con permisos adecuados.

---

## 6. Enfoque de programación funcional

El objetivo de la materia es demostrar cómo pueden procesarse datos mediante funciones y transformaciones sin depender de modificar continuamente el estado del programa.

OrganiTree utilizará los siguientes conceptos de forma práctica:

| Concepto | Aplicación en OrganiTree |
|---|---|
| Funciones puras | Las funciones de búsqueda, conteo, filtrado y análisis recibirán datos y devolverán resultados sin modificar información externa. |
| Inmutabilidad | El árbol y la colección de hijos se representarán mediante tuplas, evitando modificar nodos existentes. |
| Recursión | Las funciones recorrerán un nodo y luego llamarán a la misma función para procesar sus hijos. |
| `map` | Obtener o transformar información de todos los elementos de una colección. |
| `filter` | Seleccionar empleados que cumplan una condición, por ejemplo, pertenecer a un departamento. |
| `reduce` | Acumular valores para obtener un resultado, por ejemplo, un total. |
| Composición | Combinar funciones pequeñas para realizar operaciones más completas. |
| Fold | Reducir recursivamente un árbol a un resultado, como el total de empleados o una estadística. |
| Unfold | Como ampliación, generar una estructura a partir de una semilla y una regla que indique sus hijos. |
| Pattern matching | Distinguir casos estructurales sencillos, como un nodo hoja (sin hijos) y un nodo con hijos. Se priorizará una solución comprensible; si el profesor pide expresamente `match/case`, se utilizará en un ejemplo pequeño. |
| Manejo de resultados | Representar una búsqueda sin coincidencias con `None` (idea similar a Maybe) y devolver estados/mensajes sencillos para validaciones (idea similar a Result), sin crear abstracciones avanzadas. |

### 6.1 Funciones puras y efectos externos

Leer un archivo, solicitar datos por teclado e imprimir en pantalla son operaciones con efectos externos. Por ello, no sería correcto afirmar que absolutamente todas las instrucciones del programa son puras.

La solución será mantener esos efectos en los lugares donde son necesarios:

- `datos.py`: lectura del archivo CSV.
- `main.py`: entrada por teclado y presentación de resultados.

Los módulos `arbol.py` y `analisis.py` contendrán principalmente operaciones que reciben datos y devuelven resultados. Siempre que sea posible, estas funciones no modificarán las estructuras originales ni dependerán de variables globales.

### 6.2 Representación inmutable

La estructura se construirá conceptualmente como un nodo que contiene:

1. Los datos necesarios del empleado.
2. Una tupla con sus nodos hijos.

Ejemplo conceptual:

```python
nodo = (empleado, (hijo_1, hijo_2, hijo_3))
```

La representación definitiva deberá mantener los datos internos en estructuras inmutables. No se utilizarán listas modificables para almacenar los hijos del árbol final.

### 6.3 Recorridos

- **Preorden:** procesa primero el nodo actual y después sus hijos.
- **Postorden:** procesa primero los hijos y al final el nodo actual.

Estos recorridos permitirán obtener listas de empleados, mostrar el organigrama y calcular estadísticas.

### 6.4 Pattern matching

El proyecto necesita distinguir entre diferentes formas de un nodo. El caso más sencillo es identificar si un nodo es una hoja (no tiene hijos) o una rama (tiene uno o más hijos). Primero se resolverá con condiciones fáciles de explicar. Si se requiere mostrar el `match/case` de Python, se agregará un ejemplo pequeño que reconozca esos dos casos, sin convertirlo en una estructura compleja.

### 6.5 Funciones de orden superior

El proyecto demostrará las operaciones solicitadas con ejemplos relacionados con los empleados:

- `map`: obtener una colección con los nombres de todos los empleados.
- `filter`: seleccionar los empleados de un departamento.
- `reduce`: acumular la cantidad de empleados o sumar valores de una colección.

No se utilizarán estas herramientas solo por cumplir una lista. Cada operación deberá tener un propósito claro dentro del análisis.

---

## 7. Organización de carpetas y archivos

La estructura acordada del repositorio será la siguiente:

```text
OrganiTree/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── README.md
│   └── HRDataset_v14.csv       # archivo local; no se sube a GitHub
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── datos.py
│   ├── arbol.py
│   └── analisis.py
│
├── tests/
│   ├── test_datos.py
│   ├── test_arbol.py
│   └── test_analisis.py
│
└── docs/
    ├── arquitectura.md
    └── referencias.md
```

### 7.1 Archivos principales

| Archivo | Función |
|---|---|
| `README.md` | Documento principal del repositorio. Explica el proyecto, objetivos, dataset, estructura, integrantes, instalación, funcionamiento, pruebas, propuesta de emprendimiento y referencias. |
| `requirements.txt` | Lista de dependencias externas necesarias para ejecutar el proyecto. En la primera versión no se requieren paquetes externos. |
| `.gitignore` | Indica qué archivos y carpetas no deben enviarse a GitHub, como el entorno virtual, archivos temporales de Python y el CSV del dataset. |
| `data/README.md` | Explica dónde descargar el dataset, qué nombre debe tener el CSV y cómo colocarlo localmente. También recuerda las condiciones de uso de la fuente. |
| `docs/arquitectura.md` | Describe cómo se conectan los módulos, qué información recibe y entrega cada uno y las decisiones tomadas para representar el árbol. |
| `docs/referencias.md` | Contiene las cinco referencias académicas seleccionadas, sus enlaces y una breve explicación de su relación con el proyecto. |

### 7.2 Módulos de `src/`

| Archivo | Responsabilidad |
|---|---|
| `__init__.py` | Identifica `src` como paquete de Python. Puede permanecer vacío. |
| `main.py` | Punto de entrada. Presenta el menú, solicita opciones, llama a las funciones de los otros módulos y muestra los resultados. No debe concentrar la lógica de análisis. |
| `datos.py` | Abre el CSV, lee los registros, selecciona los campos necesarios y realiza validaciones relacionadas con la entrada. Es el único módulo encargado de leer el archivo. |
| `arbol.py` | Define la representación del árbol, normaliza nombres para relacionar gerentes y empleados, construye la estructura y contiene los recorridos recursivos y operaciones propias del árbol. |
| `analisis.py` | Contiene las búsquedas, filtros, estadísticas y análisis sobre el árbol ya construido. Aquí se aplicarán `map`, `filter`, `reduce` y composición cuando sean útiles. |

### 7.3 Archivos de `tests/`

| Archivo | Qué comprobará |
|---|---|
| `test_datos.py` | Lectura de registros, campos faltantes, archivo inexistente e identificadores duplicados. |
| `test_arbol.py` | Construcción de un árbol pequeño, relaciones padre-hijo, recorridos, altura e inmutabilidad. |
| `test_analisis.py` | Búsquedas existentes y no existentes, filtros, conteos, subordinados y estadísticas. |

Las pruebas utilizarán ejemplos pequeños creados por el equipo. Así podrán comprobar la lógica sin depender de que el dataset completo esté disponible en cada prueba.

---

## 8. División del trabajo del equipo

Se utilizará la **Estrategia 1: división por módulos técnicos**. Cada integrante será responsable de un módulo principal y tendrá tareas definidas en GitHub Issues.

### 8.1 Integrante 1 — Arturo Cortés García

**Responsable principal:** `src/datos.py`  
**Módulo asignado:** lectura, preparación y validación de datos.

**Responsabilidades:**

1. Descargar y revisar el dataset seleccionado.
2. Identificar los encabezados del CSV que utilizará el proyecto.
3. Implementar la lectura del archivo.
4. Extraer los datos necesarios: identificador, nombre, gerente, identificador de gerente, departamento, puesto y estado laboral.
5. Revisar campos indispensables vacíos.
6. Detectar identificadores de empleados repetidos.
7. Preparar los registros en una estructura que pueda recibir `arbol.py`.
8. Documentar las funciones y sus resultados.
9. Elaborar pruebas para la lectura y validación.

**Resultado esperado:** una función de lectura que reciba la ubicación del CSV y devuelva los registros preparados, además de información clara cuando el archivo o sus datos presenten problemas.

**Límite de responsabilidad:** este módulo no construye el árbol ni realiza estadísticas organizacionales. Entrega los registros preparados al módulo `arbol.py`.

### 8.2 Integrante 2 — Kevin Osvaldo Barajas Anaya

**Responsable principal:** `src/arbol.py`  
**Módulo asignado:** representación, construcción y recorridos del árbol.

**Responsabilidades:**

1. Definir la representación inmutable de un nodo y sus hijos.
2. Crear la función para normalizar nombres de empleados y gerentes.
3. Relacionar los empleados con sus supervisores cuando estos aparezcan en el CSV.
4. Construir la raíz artificial de la organización y sus ramas.
5. Identificar las relaciones que no puedan conectarse con un empleado del archivo.
6. Implementar recorridos en preorden y postorden.
7. Implementar operaciones recursivas básicas, como altura y conteo de nodos.
8. Procurar que las operaciones no modifiquen el árbol original.
9. Elaborar pruebas con árboles pequeños.
10. Documentar el funcionamiento y las condiciones de sus funciones.

**Resultado esperado:** una función que reciba los registros preparados y devuelva el árbol organizacional, junto con funciones para recorrer y obtener información estructural.

**Límite de responsabilidad:** este módulo no lee directamente el CSV ni administra el menú. Recibe los registros de `datos.py` y entrega el árbol a `analisis.py` y `main.py`.

### 8.3 Integrante 3 — Kevin Guadalupe López Vega

**Responsable principal:** `src/analisis.py` y coordinación de `src/main.py`.  
**Módulo asignado:** consultas, estadísticas e integración del programa.

**Responsabilidades:**

1. Definir junto con el equipo las operaciones que ofrecerá el sistema.
2. Implementar búsquedas por identificador y nombre.
3. Consultar subordinados directos y, cuando corresponda, subordinados de niveles inferiores.
4. Filtrar empleados por departamento o estado laboral.
5. Calcular estadísticas generales de la organización.
6. Identificar gerentes con muchos subordinados directos mediante un umbral configurable.
7. Identificar departamentos con mayor cantidad de empleados.
8. Mostrar advertencias de relaciones jerárquicas no resueltas que reciba de los otros módulos.
9. Aplicar `map`, `filter`, `reduce` y composición en operaciones justificadas.
10. Coordinar la integración de `datos.py`, `arbol.py` y `analisis.py` desde `main.py`.
11. Elaborar pruebas de análisis y participar en las pruebas de integración.
12. Coordinar la actualización de la documentación principal.

**Resultado esperado:** un módulo de análisis que reciba el árbol y devuelva resultados, más un programa principal que permita utilizar las funciones desde un menú de consola.

**Límite de responsabilidad:** la coordinación de `main.py` no significa que este integrante deba realizar el trabajo de los otros módulos. Cada responsable debe entregar funciones probadas y documentadas para que la integración sea compartida.

### 8.4 Responsabilidades compartidas

Aunque cada integrante tenga un módulo asignado, el proyecto es responsabilidad de los tres.

Todos deberán:

- Entender la estructura general y el flujo de información.
- Probar sus propias funciones antes de solicitar su integración.
- Revisar al menos un Pull Request de otro integrante.
- Mantener commits frecuentes y descriptivos.
- Participar en la revisión de errores de integración.
- Aportar a la documentación y referencias.
- Poder explicar el funcionamiento del sistema durante la presentación.

Los nombres de usuario de GitHub deberán agregarse en cuanto cada integrante confirme su cuenta. No se inventarán usuarios ni se dejarán como definitivos valores de ejemplo.

---

## 9. Contrato de integración entre módulos

Para evitar que cada integrante programe con una idea diferente de cómo deben conectarse las funciones, se establecerá el siguiente flujo:

```text
                  main.py
                     |
          +----------+----------+
          |                     |
       datos.py              arbol.py
          |                     |
  Registros del CSV  ------> Árbol inmutable
                                |
                            analisis.py
                                |
                    Resultados para main.py
```

### 9.1 Qué recibe y entrega cada módulo

| Módulo | Recibe | Entrega |
|---|---|---|
| `datos.py` | Ruta del CSV. | Registros preparados y advertencias de lectura o validación. |
| `arbol.py` | Registros preparados. | Árbol organizacional inmutable y advertencias de relaciones no resueltas. |
| `analisis.py` | Árbol organizacional. | Resultados de búsquedas, conteos, filtros y estadísticas. |
| `main.py` | Opciones del usuario y resultados de los módulos. | Menú y resultados presentados en consola. |

Antes de programar por separado, los integrantes deben acordar los nombres de las funciones y el formato de los datos que se intercambiarán. Si el formato cambia, se debe actualizar la documentación y avisar al resto del equipo.

### 9.2 Nombres de funciones sugeridos

Los siguientes nombres son una guía inicial; pero pueden ser ajustados siempre y cuando se conserve una interfaz común.

**`datos.py`**

- `leer_empleados(ruta)`: abre el CSV y obtiene sus registros.
- `preparar_empleados(registros)`: conserva y ordena los campos que necesita el proyecto.
- `validar_empleados(registros)`: identifica datos indispensables faltantes y posibles duplicados.

**`arbol.py`**

- `normalizar_nombre(nombre)`: prepara los nombres para compararlos.
- `construir_arbol(empleados)`: crea el árbol organizacional.
- `preorden(arbol)`: obtiene los nodos primero por la raíz y luego por sus hijos.
- `postorden(arbol)`: obtiene los nodos primero por sus hijos y al final por la raíz.
- `calcular_altura(arbol)`: obtiene la cantidad de niveles de la estructura.

**`analisis.py`**

- `buscar_por_id(arbol, identificador)`: localiza un empleado por su identificador.
- `buscar_por_nombre(arbol, nombre)`: localiza coincidencias por nombre.
- `obtener_subordinados(arbol, identificador)`: obtiene subordinados del empleado indicado.
- `filtrar_por_departamento(empleados, departamento)`: selecciona empleados de un departamento.
- `calcular_estadisticas(arbol)`: reúne las estadísticas generales.
- `gerentes_con_muchos_subordinados(arbol, umbral)`: identifica gerentes que superan el límite indicado.

**`main.py`**

- `mostrar_menu()`: presenta las opciones disponibles.
- `ejecutar_opcion(opcion, arbol)`: llama a la operación correspondiente y muestra el resultado.
- `main()`: organiza la ejecución general.

---

## 10. Propuesta de menú del sistema

El programa se ejecutará desde la terminal. El menú puede tener las siguientes opciones:

```text
========================================
          ORGANITREE
 Analizador de estructuras jerárquicas
========================================

1. Mostrar organigrama
2. Buscar empleado por ID
3. Buscar empleado por nombre
4. Mostrar subordinados de un empleado
5. Consultar estadísticas generales
6. Filtrar empleados por departamento
7. Mostrar gerentes con más subordinados
8. Mostrar departamentos con más empleados
9. Mostrar advertencias de relaciones jerárquicas
0. Salir

Seleccione una opción:
```

El menú es una propuesta de interacción; puede reducirse si el tiempo disponible lo requiere. La lógica de búsqueda y análisis deberá permanecer en sus módulos correspondientes, no dentro de `main.py`.

---

## 11. Análisis organizacional y componente de emprendimiento

### 11.1 Nombre de la propuesta

**OrganiTree — Analizador de estructuras organizacionales.**

### 11.2 Problema identificado

Las pequeñas y medianas empresas pueden tener información de su personal distribuida en hojas de cálculo o archivos. Cuando no existe una representación clara de las relaciones de supervisión, puede resultar difícil identificar cómo se distribuyen las responsabilidades, cuántas personas dependen de cada gerente o qué áreas concentran más colaboradores.

### 11.3 Propuesta de valor

OrganiTree transforma un archivo de empleados en una estructura jerárquica consultable y genera indicadores sencillos que ayudan a comprender la organización.

Su valor no consiste únicamente en dibujar un organigrama. También permite explorar relaciones y señalar registros o distribuciones que podrían necesitar una revisión administrativa.

### 11.4 Análisis que puede ofrecer

**A. Gerentes con demasiados subordinados directos**

El programa contará cuántos empleados reportan directamente a cada gerente. Después comparará el resultado con un umbral definido por el usuario o por la organización.

Ejemplo ilustrativo: si el umbral configurado es de 10 subordinados directos, el sistema mostrará los gerentes que tengan más de 10 personas a su cargo directamente.

El umbral no representa una regla universal ni demuestra por sí solo que exista un problema. Es un criterio configurable para señalar estructuras que podrían revisarse.

**B. Departamentos con estructuras extensas**

El sistema contará cuántos empleados pertenecen a cada departamento y permitirá ordenar los resultados de mayor a menor. En una ampliación, también podría comparar la cantidad de niveles o gerentes dentro de cada departamento.

Un departamento con más empleados no necesariamente es ineficiente. El resultado es un indicador descriptivo y no una evaluación automática de su desempeño.

**C. Problemas en las relaciones jerárquicas**

El programa podrá advertir situaciones como:

- Un empleado con `EmpID` duplicado.
- Un registro sin nombre o identificador indispensable.
- Un `ManagerName` vacío.
- Un supervisor cuyo nombre no coincide con ningún empleado del archivo.
- Un mismo `ManagerID` asociado a nombres diferentes.
- Una relación circular que impida construir un árbol válido.

Estas advertencias servirán para revisar la calidad de los datos. No se debe modificar una relación automáticamente sin contar con información que justifique el cambio.

**D. Comprensión de niveles y subordinación**

El sistema permitirá conocer la altura del árbol, la cantidad de subordinados directos de un gerente y la distribución de los empleados a través de los niveles jerárquicos.

### 11.5 Mercado objetivo

- Pequeñas y medianas empresas.
- Áreas de recursos humanos.
- Consultorías de administración y organización empresarial.
- Organizaciones que mantienen sus registros de personal en hojas de cálculo.

### 11.6 Modelo de monetización propuesto

Como idea de negocio futura, el sistema podría ofrecerse mediante:

1. **Licencia de uso:** pago por utilizar una versión instalada del analizador.
2. **Suscripción:** pago mensual por utilizar una versión con funciones ampliadas.
3. **Servicio de configuración:** apoyo para adaptar el sistema a los formatos de datos de una empresa.
4. **Reportes personalizados:** generación de análisis y reportes organizacionales adicionales.

Estas opciones son hipótesis de monetización para el componente de emprendimiento. No forman parte de las funcionalidades que se deben programar en esta entrega.

### 11.7 Diferenciador

La propuesta integra la construcción automática de una jerarquía con operaciones de análisis sobre la estructura. En vez de limitarse a presentar una tabla de empleados, permite navegar relaciones de supervisión, localizar posibles inconsistencias y obtener indicadores organizacionales básicos a partir de un CSV.

### 11.8 Limitaciones de la propuesta

- El sistema no determina por sí solo si una estructura es buena o mala.
- Tener muchos subordinados no demuestra automáticamente una sobrecarga de trabajo.
- Tener muchos empleados en un departamento no demuestra ineficiencia.
- Las advertencias dependen de que los datos de entrada estén completos y correctamente registrados.
- El dataset seleccionado es sintético y solo sirve para demostrar el funcionamiento; no valida la viabilidad comercial con empresas reales.
- Una implementación comercial requeriría revisar privacidad, permisos de uso y seguridad de los datos de cada organización.

---

## 12. Decisiones y límites del proyecto

Para mantener una implementación sencilla, comprensible y acorde con el nivel actual del equipo, se establecen las siguientes decisiones:

- El lenguaje principal será Python.
- El programa funcionará en consola.
- La fuente de datos será un CSV descargado de Kaggle.
- La estructura principal será un árbol organizacional.
- Se priorizarán funciones pequeñas, nombres descriptivos y comentarios en español.
- Se utilizarán módulos de la biblioteca estándar de Python siempre que sea suficiente.
- No se utilizarán `networkx`, `anytree`, `toolz` ni otras librerías para realizar automáticamente las operaciones centrales que el equipo debe implementar.
- No se desarrollará una aplicación web, una API, una interfaz gráfica ni una conexión a un gestor de bases de datos en esta primera versión.
- No se modificarán directamente los datos originales del CSV.
- No se presentarán los indicadores como diagnósticos definitivos de eficiencia empresarial.
- Las ampliaciones avanzadas se abordarán únicamente después de completar y probar el sistema básico.

Estas decisiones no buscan evitar el aprendizaje de programación funcional. Buscan concentrar el trabajo en comprender y demostrar correctamente sus fundamentos, en lugar de incorporar herramientas y abstracciones que el equipo todavía no ha estudiado.
