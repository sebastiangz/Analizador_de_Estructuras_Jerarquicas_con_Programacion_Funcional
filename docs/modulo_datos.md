# Guía del módulo `datos.py`

Esta guía explica la parte del proyecto asignada a Arturo Cortés García: leer, seleccionar, preparar y validar los datos de empleados que se utilizarán para construir el árbol organizacional.

## 1. ¿Cuál es la función de este módulo?

El módulo `datos.py` se encarga de obtener la información del archivo CSV y prepararla para que el módulo `arbol.py` pueda utilizarla.

El proyecto utiliza el conjunto de datos **Human Resources Data Set — Dental Magic**, que contiene información de empleados, sus puestos, departamentos y supervisores.

Las responsabilidades de este módulo son:

- Leer el archivo CSV.
- Obtener los registros de empleados.
- Seleccionar los campos necesarios.
- Detectar datos indispensables faltantes.
- Identificar identificadores de empleados duplicados.
- Entregar los registros preparados al módulo `arbol.py`.

Este módulo no construye el árbol ni realiza estadísticas organizacionales.

## 2. ¿Qué información se utilizará?

El archivo original contiene varias columnas, pero OrganiTree solamente necesita siete campos:

| Campo del CSV | Descripción |
|---|---|
| `EmpID` | Identificador del empleado. |
| `Employee_Name` | Nombre del empleado. |
| `ManagerName` | Nombre de su supervisor. |
| `ManagerID` | Identificador del gerente registrado. |
| `Department` | Departamento al que pertenece. |
| `Position` | Puesto del empleado. |
| `EmploymentStatus` | Estado laboral del empleado. |

Se conservarán los nombres originales de las columnas para que los demás módulos puedan reconocerlos sin tener que cambiar su estructura.

## 3. Lectura del archivo CSV

La función principal para leer el archivo será:

```python
leer_empleados(ruta)
```

Recibe la ubicación del archivo CSV y devuelve una lista de diccionarios. Cada diccionario representa un empleado y contiene los valores de sus columnas.

Ejemplo:

```python
empleados = leer_empleados("data/HRDataset_v14.csv")
```

El resultado tendrá una estructura similar a esta:

```python
[
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
```

Se utiliza `csv.DictReader` porque permite acceder a los valores mediante el nombre de cada columna, en lugar de utilizar posiciones numéricas.

## 4. Selección de campos

La función:

```python
preparar_empleados(registros)
```

Recibe los registros obtenidos del CSV y conserva únicamente los siete campos que necesita el proyecto.

Esto permite trabajar con información más sencilla y evita utilizar columnas que no tienen relación con el análisis jerárquico.

La función no modifica los registros originales, sino que genera una nueva lista con los campos seleccionados.

## 5. Validación de los registros

Antes de entregar los datos al módulo `arbol.py`, es necesario revisar que tengan la información básica para construir la estructura organizacional.

La función:

```python
validar_empleados(registros)
```

Revisa las siguientes situaciones:

### 5.1 Identificadores faltantes

Cada empleado debe tener un valor en `EmpID`.

Si un registro no tiene identificador, se genera una advertencia porque no se puede identificar correctamente al empleado.

### 5.2 Nombres faltantes

Cada registro debe tener un valor en `Employee_Name`.

Si falta el nombre, se genera una advertencia porque no se puede reconocer al empleado dentro de la organización.

### 5.3 Identificadores duplicados

Dos empleados no deben compartir el mismo `EmpID`.

Por ejemplo:

```text
Empleado 1: EmpID = 10
Empleado 2: EmpID = 10
```

Esta situación genera una advertencia porque puede provocar confusiones al construir el árbol.

### 5.4 Información del gerente

El campo `ManagerName` puede estar vacío o contener el nombre de un supervisor que no aparece entre los empleados del archivo.

El módulo de datos conserva esa información y no inventa un gerente para completar el registro.

La identificación de supervisores externos, la comparación de nombres y la construcción de las relaciones corresponden al módulo `arbol.py`.

## 6. Preparación y entrega de los datos

Una vez leídos, seleccionados y revisados los registros, se entregarán al módulo `arbol.py`.

El flujo de trabajo será:

```text
Archivo CSV
    |
    v
leer_empleados()
    |
    v
preparar_empleados()
    |
    v
validar_empleados()
    |
    v
Lista de diccionarios
    |
    v
construir_arbol()
```

La información se entregará conservando los encabezados originales:

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
```

El módulo `arbol.py` recibirá esta lista y se encargará de convertir los registros en tuplas y construir las relaciones entre gerentes y empleados.

## 7. Funciones del módulo

El archivo `src/datos.py` tendrá las siguientes funciones principales:

| Función | Responsabilidad |
|---|---|
| `leer_empleados(ruta)` | Abre el archivo CSV y obtiene los registros. |
| `preparar_empleados(registros)` | Selecciona los siete campos necesarios. |
| `validar_empleados(registros)` | Detecta campos indispensables faltantes e identificadores duplicados. |

Estas funciones se mantienen separadas para que cada una tenga una responsabilidad específica y sea más fácil comprobar su funcionamiento.

## 8. Programación funcional en el módulo

Aunque la lectura de un archivo es una operación que tiene efectos externos, el procesamiento de los registros puede realizarse de forma sencilla siguiendo principios de programación funcional.

En este módulo se aplicarán los siguientes conceptos:

- **Funciones pequeñas:** cada función realiza una tarea específica.
- **Inmutabilidad:** los registros originales no se modifican directamente; se generan nuevas estructuras cuando se seleccionan los campos.
- **Funciones puras:** las funciones de preparación y validación reciben registros y devuelven resultados sin modificar información externa.
- **Separación de efectos:** la lectura del archivo se mantiene en `leer_empleados`, evitando mezclarla con las funciones de validación y preparación.

## 9. Manejo de errores

El módulo debe contemplar situaciones que pueden impedir la lectura correcta de los datos:

- Que el archivo CSV no exista.
- Que el archivo esté vacío.
- Que falten encabezados necesarios.
- Que existan identificadores o nombres indispensables vacíos.
- Que existan identificadores duplicados.

Cuando el archivo no pueda leerse o no contenga los encabezados necesarios, la función de lectura deberá informar el problema mediante un mensaje claro.

Las advertencias de validación se conservarán para que puedan revisarse antes de construir el árbol.

## 10. Pruebas

Las pruebas de este módulo se encontrarán en:

```text
tests/test_datos.py
```

Se utilizarán archivos CSV pequeños y registros de ejemplo para comprobar las funciones sin depender de descargar el dataset completo.

Los casos principales serán:

- Lectura correcta de un archivo CSV.
- Selección de los campos necesarios.
- Detección de identificadores duplicados.
- Detección de identificadores o nombres faltantes.
- Manejo de un archivo inexistente.

Las pruebas se ejecutarán desde la carpeta principal del proyecto con:

```bash
python -m unittest discover -s tests -v
```

## 11. Límites del módulo

Para mantener separadas las responsabilidades del equipo, este módulo no realizará las siguientes operaciones:

- No construirá el árbol organizacional.
- No normalizará los nombres de empleados y gerentes.
- No buscará subordinados.
- No calculará la altura ni los niveles del árbol.
- No realizará estadísticas por departamento.
- No mostrará el menú del programa.

Estas operaciones corresponden a `arbol.py`, `analisis.py` y `main.py`.

El objetivo de `datos.py` es entregar información correctamente leída, organizada y revisada para que los demás módulos puedan trabajar con ella.