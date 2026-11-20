# Organización de carpetas y archivos

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
    ├── modulo_arbol.md
    ├── modulo_datos.md
    ├── modulo_analisis.md
    ├── arquitectura.md
    └── referencias.md
    
```

## Archivos principales

| Archivo | Función |
| --- | --- |
| `README.md` | Documento principal del repositorio. Explica el proyecto, objetivos, dataset, estructura, integrantes, instalación, funcionamiento, pruebas, propuesta de emprendimiento y referencias. |
| `requirements.txt` | Lista de dependencias externas necesarias para ejecutar el proyecto. En la primera versión no se requieren paquetes externos. |
| `.gitignore` | Indica qué archivos y carpetas no deben enviarse a GitHub, como el entorno virtual, archivos temporales de Python y el CSV del dataset. |
| `data/README.md` | Explica dónde descargar el dataset, qué nombre debe tener el CSV y cómo colocarlo localmente. También recuerda las condiciones de uso de la fuente. |
| `docs/arquitectura.md` | Describe cómo se conectan los módulos, qué información recibe y entrega cada uno y las decisiones tomadas para representar el árbol. |
| `docs/referencias.md` | Contiene las cinco referencias académicas seleccionadas, sus enlaces y una breve explicación de su relación con el proyecto. |

## Módulos de `src/`

| Archivo | Responsabilidad |
| --- | --- |
| `__init__.py` | Identifica `src` como paquete de Python. Puede permanecer vacío. |
| `main.py` | Punto de entrada. Presenta el menú, solicita opciones, llama a las funciones de los otros módulos y muestra los resultados. No debe concentrar la lógica de análisis. |
| `datos.py` | Abre el CSV, lee los registros, selecciona los campos necesarios y realiza validaciones relacionadas con la entrada. Es el único módulo encargado de leer el archivo. |
| `arbol.py` | Define la representación del árbol, normaliza nombres para relacionar gerentes y empleados, construye la estructura y contiene los recorridos recursivos y operaciones propias del árbol. |
| `analisis.py` | Contiene las búsquedas, filtros, estadísticas y análisis sobre el árbol ya construido. Aquí se aplicarán `map`, `filter`, `reduce` y composición cuando sean útiles. |

## Archivos de `tests/`

| Archivo | Qué comprobará |
| --- | --- |
| `test_datos.py` | Lectura de registros, campos faltantes, archivo inexistente e identificadores duplicados. |
| `test_arbol.py` | Construcción de un árbol pequeño, relaciones padre-hijo, recorridos, altura e inmutabilidad. |
| `test_analisis.py` | Búsquedas existentes y no existentes, filtros, conteos, subordinados y estadísticas. |

Las pruebas utilizarán ejemplos pequeños creados por el equipo. Así podrán comprobar la lógica sin depender de que el dataset completo esté disponible en cada prueba.
