# 🌳 Proyecto 4: Analizador de Estructuras Jerárquicas con Programación Funcional

## 📋 Descripción del Proyecto

Sistema funcional para procesar y analizar estructuras de datos jerárquicas (árboles, grafos, JSON anidado, XML) mediante recursión, fold/unfold, traversal funcional y transformaciones inmutables.

**Universidad de Colima - Ingeniería en Computación Inteligente**  
**Materia**: Programación Funcional  
**Profesor**: Gonzalez Zepeda Sebastian  
**Semestre**: Agosto 2025 - Enero 2026

---

## 🎯 Objetivos

- Implementar **recursión funcional** para árboles y grafos
- Aplicar **fold/unfold (catamorphisms/anamorphisms)** en estructuras recursivas
- Desarrollar **traversal funcional** (preorder, inorder, postorder)
- Utilizar **pattern matching** para análisis estructural
- Crear **zippers funcionales** para navegación eficiente
- Practicar **transformaciones inmutables** en estructuras complejas

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje**: Python 3.11+
- **Paradigma**: Programación Funcional
- **Librerías**:
  - `dataclasses` - Estructuras inmutables
  - `toolz` - Utilidades funcionales
  - `networkx` - Análisis de grafos
  - `anytree` - Manipulación de árboles
  - `graphviz` - Visualización

---

## 📦 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/sebastiangz/Analizador_de_Estructuras_Jerarquicas_con_Programacion_Funcional
cd hierarchical-analyzer

# Crear entorno virtual
python -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### requirements.txt
```
toolz>=0.12.0
networkx>=3.2.0
anytree>=2.12.0
graphviz>=0.20.0
typing-extensions>=4.8.0
```

---

## 🚀 Uso del Sistema

```python
from src.tree import Tree, fold, unfold
from src.traversal import preorder, postorder

# Crear árbol funcional
tree = Tree.branch(
    value=1,
    children=[
        Tree.leaf(2),
        Tree.branch(3, [Tree.leaf(4), Tree.leaf(5)]),
        Tree.leaf(6)
    ]
)

# Fold: calcular suma de todos los nodos
total = fold(
    tree,
    leaf_fn=lambda x: x,
    branch_fn=lambda val, children: val + sum(children)
)

# Unfold: generar árbol desde semilla
fibonacci_tree = unfold(
    seed=1,
    predicate=lambda n: n < 100,
    generator=lambda n: [n * 2, n * 3]
)

# Traversal funcional
values = preorder(tree, lambda node: node.value)
```

---

## 📂 Estructura del Proyecto

```
hierarchical-analyzer/
├── src/
│   ├── __init__.py
│   ├── tree.py             # Estructuras de árbol funcionales
│   ├── graph.py            # Operaciones en grafos
│   ├── traversal.py        # Algoritmos de recorrido
│   ├── fold_unfold.py      # Catamorphisms y anamorphisms
│   ├── zipper.py           # Zippers funcionales
│   ├── transform.py        # Transformaciones
│   └── visualization.py    # Generación de gráficos
├── tests/
│   ├── test_tree.py
│   ├── test_graph.py
│   ├── test_fold.py
│   └── test_zipper.py
├── examples/
│   ├── json_analyzer.py    # Análisis de JSON anidado
│   ├── filesystem.py       # Navegación de directorios
│   └── dom_parser.py       # Parser de HTML/XML
├── docs/
│   ├── recursion_patterns.md
│   └── api_reference.md
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🔑 Características Principales

### 1. Estructuras de Datos Funcionales
```python
from dataclasses import dataclass
from typing import Generic, TypeVar, List

T = TypeVar('T')

@dataclass(frozen=True)
class Tree(Generic[T]):
    value: T
    children: tuple['Tree[T]', ...] = ()
    
    @staticmethod
    def leaf(value: T) -> 'Tree[T]':
        return Tree(value, ())
    
    @staticmethod
    def branch(value: T, children: List['Tree[T]']) -> 'Tree[T]':
        return Tree(value, tuple(children))
    
    def map(self, fn) -> 'Tree':
        """Functor map para árboles"""
        return Tree(
            fn(self.value),
            tuple(child.map(fn) for child in self.children)
        )
```

### 2. Fold/Unfold (Catamorphism/Anamorphism)
```python
from typing import Callable, TypeVar

A = TypeVar('A')
B = TypeVar('B')

def fold(tree: Tree[A], 
         leaf_fn: Callable[[A], B],
         branch_fn: Callable[[A, List[B]], B]) -> B:
    """
    Catamorphism: consume árbol de abajo hacia arriba
    """
    if not tree.children:
        return leaf_fn(tree.value)
    
    children_results = [fold(child, leaf_fn, branch_fn) 
                       for child in tree.children]
    return branch_fn(tree.value, children_results)

def unfold(seed: A,
           predicate: Callable[[A], bool],
           generator: Callable[[A], List[A]]) -> Tree[A]:
    """
    Anamorphism: genera árbol de arriba hacia abajo
    """
    if not predicate(seed):
        return Tree.leaf(seed)
    
    children = [unfold(child, predicate, generator) 
                for child in generator(seed)]
    return Tree.branch(seed, children)
```

### 3. Zipper Funcional (Navegación Eficiente)
```python
@dataclass(frozen=True)
class TreeZipper(Generic[T]):
    """Zipper para navegación eficiente en árboles"""
    focus: Tree[T]
    context: tuple  # Breadcrumbs
    
    def up(self) -> 'TreeZipper[T]':
        """Mover hacia el padre"""
        if not self.context:
            return self
        parent_val, left, right, ctx = self.context
        new_tree = Tree.branch(
            parent_val,
            list(left) + [self.focus] + list(right)
        )
        return TreeZipper(new_tree, ctx)
    
    def down(self, index: int = 0) -> 'TreeZipper[T]':
        """Mover hacia un hijo"""
        if not self.focus.children:
            return self
        children = list(self.focus.children)
        new_context = (
            self.focus.value,
            tuple(children[:index]),
            tuple(children[index+1:]),
            self.context
        )
        return TreeZipper(children[index], new_context)
    
    def modify(self, fn: Callable[[T], T]) -> 'TreeZipper[T]':
        """Modificar nodo actual"""
        new_focus = Tree(fn(self.focus.value), self.focus.children)
        return TreeZipper(new_focus, self.context)
```

### 4. Traversal Funcional
```python
def preorder(tree: Tree[T], fn: Callable[[Tree[T]], A]) -> List[A]:
    """Recorrido preorden (raíz, hijos)"""
    result = [fn(tree)]
    for child in tree.children:
        result.extend(preorder(child, fn))
    return result

def postorder(tree: Tree[T], fn: Callable[[Tree[T]], A]) -> List[A]:
    """Recorrido postorden (hijos, raíz)"""
    result = []
    for child in tree.children:
        result.extend(postorder(child, fn))
    result.append(fn(tree))
    return result

def level_order(tree: Tree[T]) -> List[List[T]]:
    """Recorrido por niveles"""
    def helper(trees, acc):
        if not trees:
            return acc
        values = [t.value for t in trees]
        children = [child for t in trees for child in t.children]
        return helper(children, acc + [values])
    return helper([tree], [])
```

---

## 📊 Funcionalidades Implementadas

### Operaciones en Árboles
- ✅ Construcción funcional de árboles
- ✅ Map, Filter, Fold sobre árboles
- ✅ Búsqueda (BFS, DFS)
- ✅ Cálculo de altura, profundidad
- ✅ Balanceo de árboles

### Análisis Estructural
- ✅ Detección de patrones
- ✅ Validación de estructuras
- ✅ Estadísticas (nodos, hojas, altura)
- ✅ Comparación de árboles

### Transformaciones
- ✅ Poda funcional
- ✅ Injertos de subárboles
- ✅ Aplanamiento (flatten)
- ✅ Serialización/Deserialización

### Visualización
- ✅ Representación gráfica con Graphviz
- ✅ Exportación a DOT
- ✅ Visualización interactiva

---

## 🧪 Testing

```bash
# Ejecutar tests
pytest tests/ -v

# Tests de recursión
pytest tests/test_tree.py -k "recursive"

# Tests de propiedad
pytest tests/ -k "property"

# Cobertura
pytest --cov=src tests/
```

---

## 📈 Pipeline de Desarrollo

### Semana 1: Estructuras Básicas (30 Oct - 5 Nov)
- Implementación de Tree y Graph
- Operaciones básicas funcionales
- Recursión simple

### Semana 2: Fold/Unfold Avanzado (6 Nov - 12 Nov)
- Catamorphisms y anamorphisms
- Zippers funcionales
- Traversal completo

### Semana 3: Aplicaciones (13 Nov - 19 Nov)
- Analizador de JSON/XML
- Sistema de archivos funcional
- Visualización completa

---

## 💼 Componente de Emprendimiento

**Aplicación Real**: Herramienta de análisis de estructuras organizacionales

**Propuesta de Valor**:
- Análisis de organigramas empresariales
- Detección de ineficiencias en jerarquías
- Optimización de reporting lines
- Visualización interactiva de estructuras

**Casos de Uso**:
- Recursos Humanos: análisis de estructura organizacional
- IT: análisis de dependencias de sistemas
- Finanzas: análisis de estructuras corporativas

---

## 📚 Referencias

- Bird, R., & Wadler, P. (1988). *Introduction to Functional Programming*
- Hutton, G. (2016). *Programming in Haskell* (Tree recursion chapter)
- **Catamorphisms**: https://wiki.haskell.org/Catamorphisms
- **Zippers**: https://en.wikipedia.org/wiki/Zipper_(data_structure)

---

## 🏆 Criterios de Evaluación

- **Recursión Funcional (30%)**: Elegancia, corrección, eficiencia
- **Fold/Unfold (25%)**: Implementación correcta de morfismos
- **Zippers (20%)**: Navegación eficiente, inmutabilidad
- **Testing (15%)**: Casos edge, properties
- **Documentación (10%)**: Claridad, ejemplos

---

## 👥 Autor

**Nombre**: [Tu Nombre]  
**Email**: [tu-email@ucol.mx]  
**GitHub**: [@tu-usuario](https://github.com/tu-usuario)

---

## 📄 Licencia

Proyecto académico - Universidad de Colima © 2025
