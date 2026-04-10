"""
LABORATORIO 1 - PROCESO KDD: ANÁLISIS DEL TITANIC
==================================================
PASO 1: CARGA Y DESCRIPCIÓN DE DATOS

Descripción: En este paso cargamos el dataset y realizamos una descripción 
exhaustiva de los datos de entrada, identificando variables, tipos de datos 
y características generales del dataset.

Objetivo específico:
- Cargar el archivo train.csv
- Describir la estructura del dataset
- Identificar variables demográficas, socioeconómicas y logísticas
- Evaluar la calidad inicial de los datos
"""

import pandas as pd
import os
import numpy as np

# ============================================================================
# 1. CARGA DE DATOS
# ============================================================================
print("\n" + "="*80)
print("PASO 1: CARGA Y DESCRIPCIÓN DE DATOS")
print("="*80 + "\n")

# Obtener la ruta de la carpeta actual del script
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "train.csv")

# Cargar el dataset
df = pd.read_csv(csv_path)
print("✓ Dataset cargado exitosamente\n")

# ============================================================================
# 2. INFORMACIÓN GENERAL DEL DATASET
# ============================================================================
print("\n" + "-"*80)
print("2.1 INFORMACIÓN GENERAL DEL DATASET")
print("-"*80 + "\n")

print(f"Dimensiones del dataset: {df.shape[0]} filas × {df.shape[1]} columnas\n")

print("Información detallada del dataset:")
print(df.info())

# ============================================================================
# 3. DESCRIPCIÓN DE VARIABLES
# ============================================================================
print("\n" + "-"*80)
print("2.2 DESCRIPCIÓN DE VARIABLES")
print("-"*80 + "\n")

print("VARIABLES DISPONIBLES EN EL DATASET:\n")

variables_info = {
    "PassengerId": "ID único del pasajero (ordinal/identificador)",
    "Survived": "Variable objetivo - 1: Sobrevivió, 0: No sobrevivió (binaria)",
    "Pclass": "Clase del billete (1=Primera, 2=Segunda, 3=Tercera) - Variable socioeconómica",
    "Name": "Nombre del pasajero (texto)",
    "Sex": "Sexo (male/female) - Variable demográfica",
    "Age": "Edad en años (numérica) - Variable demográfica",
    "SibSp": "Número de hermanos/cónyuge a bordo (numérica) - Variable demográfica",
    "Parch": "Número de padres/hijos a bordo (numérica) - Variable demográfica",
    "Ticket": "Número de boleto (text/identificador)",
    "Fare": "Tarifa pagada en libras esterlinas (numérica) - Variable socioeconómica",
    "Cabin": "Número de camarote (texto/ubicación) - Variable logística",
    "Embarked": "Puerto de embarque (C=Cherburgo, Q=Queenstown, S=Southampton) - Variable logística"
}

for var, desc in variables_info.items():
    print(f"  • {var:15} → {desc}")

# ============================================================================
# 4. ESTADÍSTICAS DESCRIPTIVAS
# ============================================================================
print("\n" + "-"*80)
print("2.3 ESTADÍSTICAS DESCRIPTIVAS BÁSICAS")
print("-"*80 + "\n")

print(df.describe())

# ============================================================================
# 5. ANÁLISIS DE VALORES NULOS
# ============================================================================
print("\n" + "-"*80)
print("2.4 ANÁLISIS DE VALORES NULOS (MISSING VALUES)")
print("-"*80 + "\n")

missing_data = pd.DataFrame({
    'Variable': df.columns,
    'Valores Nulos': df.isnull().sum(),
    'Porcentaje Nulos': (df.isnull().sum() / len(df) * 100).round(2)
})

missing_data = missing_data[missing_data['Valores Nulos'] > 0].reset_index(drop=True)
print(missing_data.to_string(index=False))

print(f"\nTotal de valores nulos en el dataset: {df.isnull().sum().sum()}")

# ============================================================================
# 6. ANÁLISIS DE VARIABLES CATEGÓRICAS
# ============================================================================
print("\n" + "-"*80)
print("2.5 ANÁLISIS DE VARIABLES CATEGÓRICAS")
print("-"*80 + "\n")

print("Variable objetivo - SURVIVED:")
print(df['Survived'].value_counts())
print(f"\nProporción de supervivencia:")
print(df['Survived'].value_counts(normalize=True).round(4))

print("\n\nSEXO (Sex):")
print(df['Sex'].value_counts())

print("\n\nCLASE DE BILLETE (Pclass):")
print(df['Pclass'].value_counts().sort_index())

print("\n\nPUERTO DE EMBARQUE (Embarked):")
print(df['Embarked'].value_counts())

# ============================================================================
# 7. DUPLICADOS
# ============================================================================
print("\n" + "-"*80)
print("2.6 ANÁLISIS DE DUPLICADOS")
print("-"*80 + "\n")

print(f"Número de filas duplicadas (completas): {df.duplicated().sum()}")

# ============================================================================
# 8. RESUMEN EJECUTIVO
# ============================================================================
print("\n" + "="*80)
print("RESUMEN EJECUTIVO DEL PASO 1")
print("="*80 + "\n")

resumen = f"""
DATOS CARGADOS:
  • Total de registros: {df.shape[0]}
  • Total de variables: {df.shape[1]}
  • Tasa de supervivencia: {(df['Survived'].sum()/len(df)*100):.2f}%

CALIDAD DE DATOS:
  • Valores nulos principales:
    - Age: {df['Age'].isnull().sum()} registros ({df['Age'].isnull().sum()/len(df)*100:.2f}%)
    - Cabin: {df['Cabin'].isnull().sum()} registros ({df['Cabin'].isnull().sum()/len(df)*100:.2f}%)
    - Embarked: {df['Embarked'].isnull().sum()} registros ({df['Embarked'].isnull().sum()/len(df)*100:.2f}%)
  • Variables con duplicados: {df.duplicated().sum()}

PRÓXIMOS PASOS:
  1. Limpieza y preprocesamiento de datos
  2. Análisis exploratorio (EDA)
  3. Transformación y Feature Engineering
  4. Selección y entrenamiento del modelo
  5. Evaluación e interpretación
"""

print(resumen)

print("\n✓ PASO 1 COMPLETADO\n")

# Guardar información para pasos posteriores
df.to_csv(os.path.join(script_dir, "df_original.csv"), index=False)
print(f"Dataset original guardado en: df_original.csv")
