# Análisis organizacional y componente de emprendimiento

## Nombre de la propuesta

**OrganiTree — Analizador de estructuras organizacionales.**

## Problema identificado

Las pequeñas y medianas empresas pueden tener información de su personal distribuida en hojas de cálculo o archivos. Cuando no existe una representación clara de las relaciones de supervisión, puede resultar difícil identificar cómo se distribuyen las responsabilidades, cuántas personas dependen de cada gerente o qué áreas concentran más colaboradores.

## Propuesta de valor

OrganiTree transforma un archivo de empleados en una estructura jerárquica consultable y genera indicadores sencillos que ayudan a comprender la organización.

Su valor no consiste únicamente en dibujar un organigrama. También permite explorar relaciones y señalar registros o distribuciones que podrían necesitar una revisión administrativa.

## Análisis que puede ofrecer

### A. Gerentes con demasiados subordinados directos

El programa contará cuántos empleados reportan directamente a cada gerente. Después comparará el resultado con un umbral definido por el usuario o por la organización.

Ejemplo ilustrativo: si el umbral configurado es de 10 subordinados directos, el sistema mostrará los gerentes que tengan más de 10 personas a su cargo directamente.

El umbral no representa una regla universal ni demuestra por sí solo que exista un problema. Es un criterio configurable para señalar estructuras que podrían revisarse.

### B. Departamentos con estructuras extensas

El sistema contará cuántos empleados pertenecen a cada departamento y permitirá ordenar los resultados de mayor a menor. En una ampliación, también podría comparar la cantidad de niveles o gerentes dentro de cada departamento.

Un departamento con más empleados no necesariamente es ineficiente. El resultado es un indicador descriptivo y no una evaluación automática de su desempeño.

### C. Problemas en las relaciones jerárquicas

El programa podrá advertir situaciones como:

- Un empleado con `EmpID` duplicado.
- Un registro sin nombre o identificador indispensable.
- Un `ManagerName` vacío.
- Un supervisor cuyo nombre no coincide con ningún empleado del archivo.
- Un mismo `ManagerID` asociado a nombres diferentes.
- Una relación circular que impida construir un árbol válido.

Estas advertencias servirán para revisar la calidad de los datos. No se debe modificar una relación automáticamente sin contar con información que justifique el cambio.

### D. Comprensión de niveles y subordinación

El sistema permitirá conocer la altura del árbol, la cantidad de subordinados directos de un gerente y la distribución de los empleados a través de los niveles jerárquicos.

## Mercado objetivo

- Pequeñas y medianas empresas.
- Áreas de recursos humanos.
- Consultorías de administración y organización empresarial.
- Organizaciones que mantienen sus registros de personal en hojas de cálculo.

### Modelo de monetización propuesto

Como idea de negocio futura, el sistema podría ofrecerse mediante:

1. **Licencia de uso:** pago por utilizar una versión instalada del analizador.
2. **Suscripción:** pago mensual por utilizar una versión con funciones ampliadas.
3. **Servicio de configuración:** apoyo para adaptar el sistema a los formatos de datos de una empresa.
4. **Reportes personalizados:** generación de análisis y reportes organizacionales adicionales.

Estas opciones son hipótesis de monetización para el componente de emprendimiento. No forman parte de las funcionalidades que se deben programar en esta entrega.

### Diferenciador

La propuesta integra la construcción automática de una jerarquía con operaciones de análisis sobre la estructura. En vez de limitarse a presentar una tabla de empleados, permite navegar relaciones de supervisión, localizar posibles inconsistencias y obtener indicadores organizacionales básicos a partir de un CSV.

### Limitaciones de la propuesta

- El sistema no determina por sí solo si una estructura es buena o mala.
- Tener muchos subordinados no demuestra automáticamente una sobrecarga de trabajo.
- Tener muchos empleados en un departamento no demuestra ineficiencia.
- Las advertencias dependen de que los datos de entrada estén completos y correctamente registrados.
- El dataset seleccionado es sintético y solo sirve para demostrar el funcionamiento; no valida la viabilidad comercial con empresas reales.
- Una implementación comercial requeriría revisar privacidad, permisos de uso y seguridad de los datos de cada organización.
