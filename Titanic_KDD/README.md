# Titanic KDD - Guía de Ejecución

## Estructura del Proyecto

```
Titanic_KDD/
├── INFORME_FINAL.md        ← DOCUMENTO PRINCIPAL CON TODO EL ANÁLISIS
├── README.md              ← Este archivo
├── scripts/               ← Carpeta con todos los scripts Python
├── datos/                 ← Carpeta con todos los datasets CSV
└── graficos/              ← Carpeta con todos los gráficos generados
```

---

## Cómo Ejecutar los Scripts

### Opción 1: Ejecutar desde la carpeta principal (RECOMENDADO)

```bash
# Desde Titanic_KDD/
cd "c:\Repositorios\Ciencia De Datos\Titanic_KDD"

# Ejecutar cada paso en orden
python scripts/paso1_carga.py
python scripts/paso2_exploracion.py
python scripts/paso3_limpieza.py
python scripts/paso4_transformacion.py
python scripts/paso5_modelado.py
```

### Opción 2: Ejecutar con el venv (entorno virtual)

```bash
# Activar el entorno virtual
call ".venv\Scripts\activate.bat"

# Ejecutar desde la carpeta principal
python scripts/paso1_carga.py
```

### Opción 3: Ejecutar con rutas completas

```bash
cd "c:\Repositorios\Ciencia De Datos\Titanic_KDD\scripts"
python paso1_carga.py
```

---

## Explicación de Cada Script

### 1. paso1_carga.py
- **Propósito:** Cargar el dataset original y describir los datos
- **Entrada:** `datos/train.csv`
- **Salida:** `datos/df_original.csv`
- **Importancia:** Entender la estructura y calidad inicial de datos

### 2. paso2_exploracion.py
- **Propósito:** Análisis exploratorio (EDA) con gráficos
- **Entrada:** `datos/df_original.csv`
- **Salida:** Gráficos en `graficos/01_*.png`, `02_*.png`, `03_*.png`
- **Importancia:** Identificar patrones y relaciones en los datos

### 3. paso3_limpieza.py
- **Propósito:** Limpiar y preproces ar datos
- **Entrada:** `datos/df_original.csv`
- **Salida:** `datos/df_limpio.csv`
- **Importantes:** Manejo de valores nulos, eliminación de variables irrelevantes

### 4. paso4_transformacion.py
- **Propósito:** Transformar variables y crear features
- **Entrada:** `datos/df_limpio.csv`, `datos/df_original.csv`
- **Salida:** `datos/df_transformado.csv`
- **Importancia:** Feature engineering y preparación para modelado

### 5. paso5_modelado.py
- **Propósito:** Entrenar modelo de regresión logística
- **Entrada:** `datos/df_transformado.csv`
- **Salida:** Gráficos de evaluación en `graficos/04_*.png` a `07_*.png`
- **Importancia:** Crear modelo predictivo y evaluar desempeño

---

## Resultados Principales

### Modelo de Regresión Logística
- **Exactitud: 80.45%**
- **Precisión: 78.33%**
- **Recall: 68.12%**
- **ROC-AUC: 0.8569**

### Variable Más Importante
**Género (Sex):** Coeficiente = +2.494 ⭐

Las mujeres tuvieron **74.20%** de tasa de supervivencia vs **18.89%** en hombres

---

## Requisitos

```bash
Python 3.7+
pandas
numpy
matplotlib
seaborn
scikit-learn
scipy
```

### Instalar dependencias

```bash
pip install pandas numpy matplotlib seaborn scikit-learn scipy
```

---

## Contenido del Informe Final

En `INFORME_FINAL.md` encontrarás:

1. ✓ Introducción y contexto histórico
2. ✓ Objetivos del laboratorio
3. ✓ Descripción exhaustiva de datos
4. ✓ Proceso KDD en 5 pasos (detallado)
5. ✓ Resultados y descubrimientos clave
6. ✓ Conclusiones y reflexiones
7. ✓ Información técnica completa

---

## Estructura de Carpetas Explicada

### `/scripts`
Contiene los 5 scripts Python ejecutables en orden:
- Cada script usa rutas relativas `../datos/` y `../graficos/`
- Pueden ejecutarse desde la carpeta principal
- Están completamente documentados

### `/datos`
Almacena todos los archivos CSV:
- `train.csv` - Dataset original (891 pasajeros)
- `df_original.csv` - Después de paso1 (sin cambios)
- `df_limpio.csv` - Después de paso3 (preprocesado)
- `df_transformado.csv` - Después de paso4 (listo para ML)

### `/graficos`
Contiene 7 gráficos generados automáticamente:
- 3 gráficos de análisis exploratorio
- 4 gráficos de evaluación del modelo
- Todos en formato PNG (300 DPI)

### `INFORME_FINAL.md`
Documento principal con:
- Análisis completo del proceso KDD
- Interpretación de resultados
- Conclusiones y hallazgos
- Lista completa de variables críticas

---

## Notas Importantes

1. **Ejecutar en orden:** Los scripts dependen uno del otro. Ejecutarlos en secuencia.
2. **Rutas relativas:** Los scripts usan `../` para acceder a carpetas hermanas
3. **Generación automática:** Los gráficos se crean automáticamente en paso2 y paso5
4. **Sin sobrescrituras:** Si un archivo CSV existe, se reemplaza automáticamente
5. **Encoding UTF-8:** Los scripts están configurados para UTF-8

---

## Solución de Problemas

### Error: "No such file or directory"
- Asegúrate de ejecutar desde la carpeta principal `Titanic_KDD/`
- Verifica que las carpetas `datos/`, `scripts/` y `graficos/` existan

### Error de importación (ModuleNotFoundError)
```bash
pip install pandas numpy matplotlib seaborn scikit-learn scipy
```

### Error de encoding en Windows
- Los scripts usan UTF-8, debería funcionar automáticamente
- Si hay problemas, ejecuta con: `python -X utf8 scripts/paso1_carga.py`

---

## Autor
**Laboratorio 1 - Curso de Ciencia de Datos**  
Universidad de Pamplona  
Código FGA-154 v.00  
Fecha: 10 de Abril de 2026

---

## Entrega

Envía a: **abelfer.beca@unipamplona.edu.co**  
Límite: **9:00 AM**  
Archivos requeridos:
- ✓ `INFORME_FINAL.md`
- ✓ Carpeta `scripts/` (con todos los .py)
- ✓ Carpeta `datos/` (con datos procesados)
- ✓ Carpeta `graficos/` (con visualizaciones)
