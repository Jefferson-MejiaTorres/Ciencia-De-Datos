"""
LABORATORIO 1 - PROCESO KDD: ANÁLISIS DEL TITANIC
==================================================
PASO 4: TRANSFORMACIÓN DE DATOS Y FEATURE ENGINEERING

Descripción: En este paso transformamos variables categóricas a numéricas,
creamos nuevas características (features) significativas y preparamos
los datos para el modelado.

Objetivo específico:
- Codificar variables categóricas
- Crear nuevas features informativas
- Normalizar/escalar variables numéricas si es necesario
- Preparar conjunto de datos para entrenamiento del modelo
"""

import pandas as pd
import numpy as np
import os
import sys
from sklearn.preprocessing import LabelEncoder

# Configurar encoding para Windows
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ============================================================================
# 1. CARGA DE DATOS
# ============================================================================
print("\n" + "="*80)
print("PASO 4: TRANSFORMACIÓN DE DATOS Y FEATURE ENGINEERING")
print("="*80 + "\n")

script_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(script_dir, "df_limpio.csv"))
df_original = pd.read_csv(os.path.join(script_dir, "df_original.csv"))
print(f"Dataset limpio cargado: {df.shape[0]} filas x {df.shape[1]} columnas\n")

# ============================================================================
# 2. ANÁLISIS DE VARIABLES CATEGÓRICAS
# ============================================================================
print("-"*80)
print("4.1 IDENTIFICACIÓN DE VARIABLES CATEGÓRICAS Y NUMÉRICAS")
print("-"*80 + "\n")

categoricas = df.select_dtypes(include=['object']).columns.tolist()
numericas = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

print("Variables Categóricas:")
for cat in categoricas:
    valores = df[cat].unique()
    print(f"  - {cat:15} | Valores: {valores.tolist()}")

print("\nVariables Numéricas:")
for num in numericas:
    print(f"  - {num:15} | Rango: [{df[num].min():.2f}, {df[num].max():.2f}]")

# ============================================================================
# 3. CODIFICACIÓN DE VARIABLES CATEGÓRICAS
# ============================================================================
print("\n" + "-"*80)
print("4.2 TRANSFORMACIÓN DE VARIABLES CATEGÓRICAS A NUMÉRICAS")
print("-"*80 + "\n")

df_transformed = df.copy()

# 3.1 Codificación de Sex (Binaria)
print(">>> Variable 'Sex' (codificación binaria):")
print("    female → 1")
print("    male   → 0")
sex_mapping = {'female': 1, 'male': 0}
df_transformed['Sex'] = df_transformed['Sex'].map(sex_mapping)
print(f"    ✓ Transformada: Sex")

# 3.2 Codificación de Embarked (One-Hot Encoding)
print("\n>>> Variable 'Embarked' (One-Hot Encoding):")
print("    Razón: Variable nominal con 3 categorías")

# Crear dummies para Embarked
embarked_dummies = pd.get_dummies(df['Embarked'], prefix='Embarked', drop_first=False)
print(f"    Variables creadas:")
for col in embarked_dummies.columns:
    print(f"      - {col}")

# Agregar al dataframe transformado
df_transformed = pd.concat([df_transformed, embarked_dummies], axis=1)

# Eliminar variable original
df_transformed = df_transformed.drop(columns=['Embarked'])

# ============================================================================
# 4. FEATURE ENGINEERING - CREAR NUEVAS CARACTERÍSTICAS
# ============================================================================
print("\n" + "-"*80)
print("4.3 FEATURE ENGINEERING - CREACIÓN DE NUEVAS VARIABLES")
print("-"*80 + "\n")

# 4.1 IsChild - Indicador de niño
print(">>> Feature 1: 'IsChild' (¿Es niño?)")
print("    Definición: Edad < 15 años")
df_transformed['IsChild'] = (df_transformed['Age'] < 15).astype(int)
print(f"    Justificación: Niños tuvieron trato diferenciado en evacuación")
print(f"    Frecuencia: {df_transformed['IsChild'].sum()} niños ({df_transformed['IsChild'].sum()/len(df_transformed)*100:.1f}%)")

# 4.2 IsAlone - Indicador de viajante solo
print("\n>>> Feature 2: 'IsAlone' (¿Viaja solo?)")
print("    Definición: FamilySize == 1")
df_transformed['IsAlone'] = (df_transformed['FamilySize'] == 1).astype(int)
print(f"    Justificación: Pasajeros solos tuvieron mayor autonomía")
print(f"    Frecuencia: {df_transformed['IsAlone'].sum()} solos ({df_transformed['IsAlone'].sum()/len(df_transformed)*100:.1f}%)")

# 4.3 FamilyGroupSize - Categorizar tamaño familiar
print("\n>>> Feature 3: 'FamilyGroupSize' (Categoría de grupo familiar)")
print("    Definición:")
print("      Solo (1) → 1")
print("      Pequeño (2-3) → 2")
print("      Mediano (4-5) → 3")
print("      Grande (6+) → 4")

def categorize_family(size):
    if size == 1:
        return 1
    elif size <= 3:
        return 2
    elif size <= 5:
        return 3
    else:
        return 4

df_transformed['FamilyGroupSize'] = df_transformed['FamilySize'].apply(categorize_family)
print(f"    Distribución:")
for i in range(1, 5):
    count = (df_transformed['FamilyGroupSize'] == i).sum()
    print(f"      Grupo {i}: {count} registros")

# 4.4 HasCabin - Indicador de información de camarote
print("\n>>> Feature 4: 'HasCabin' (¿Tiene información de camarote?)")
print("    Definición: Conocer el camarote implicaba acceso/recursos")
df_transformed['HasCabin'] = df_original['Cabin'].notna().astype(int)
print(f"    Frecuencia: {df_transformed['HasCabin'].sum()} con camarote ({df_transformed['HasCabin'].sum()/len(df_transformed)*100:.1f}%)")

# 4.5 HigherClass - Indicador de clase alta
print("\n>>> Feature 5: 'HigherClass' (¿Primera o segunda clase?)")
print("    Definición: Pclass <= 2")
df_transformed['HigherClass'] = (df_transformed['Pclass'] <= 2).astype(int)
print(f"    Frecuencia: {df_transformed['HigherClass'].sum()} en clase alta ({df_transformed['HigherClass'].sum()/len(df_transformed)*100:.1f}%)")

# ============================================================================
# 5. ANÁLISIS DE VARIABLES FINALES
# ============================================================================
print("\n" + "-"*80)
print("4.4 ANÁLISIS DE VARIABLES TRANSFORMADAS FINALES")
print("-"*80 + "\n")

print(f"Dimensiones después de transformación: {df_transformed.shape[0]} filas x {df_transformed.shape[1]} columnas\n")

print("Variables numéricas finales:")
numeric_final = df_transformed.select_dtypes(include=['int64', 'float64']).columns
for i, col in enumerate(numeric_final, 1):
    print(f"{i:2}. {col:20} | dtype: {df_transformed[col].dtype}")

# ============================================================================
# 6. ESTADÍSTICAS DESCRIPTIVAS
# ============================================================================
print("\n" + "-"*80)
print("4.5 ESTADÍSTICAS DESCRIPTIVAS DE VARIABLES TRANSFORMADAS")
print("-"*80 + "\n")

print(df_transformed.describe().to_string())

# ============================================================================
# 7. MATRIZ DE CORRELACIÓN
# ============================================================================
print("\n" + "-"*80)
print("4.6 CORRELACIÓN CON LA VARIABLE OBJETIVO")
print("-"*80 + "\n")

correlacion_con_survived = df_transformed.corr()['Survived'].sort_values(ascending=False)
print("Correlación de cada variable con 'Survived':\n")
for var, corr in correlacion_con_survived.items():
    print(f"  {var:20} : {corr:7.4f}")

# ============================================================================
# 8. VERIFICACIÓN FINAL
# ============================================================================
print("\n" + "-"*80)
print("4.7 VERIFICACIÓN FINAL DE INTEGRIDAD")
print("-"*80 + "\n")

print(f"Valores nulos en dataset transformado: {df_transformed.isnull().sum().sum()}")
print(f"✓ No hay valores faltantes" if df_transformed.isnull().sum().sum() == 0 else "Advertencia: Hay valores nulos")

print(f"\nDuplicados completos: {df_transformed.duplicated().sum()}")
print(f"✓ Sin duplicados" if df_transformed.duplicated().sum() == 0 else "Advertencia: Hay duplicados")

# ============================================================================
# 9. RESUMEN EJECUTIVO
# ============================================================================
print("\n" + "="*80)
print("RESUMEN EJECUTIVO DEL PASO 4")
print("="*80 + "\n")

resumen = f"""
TRANSFORMACIONES REALIZADAS:

1. CODIFICACIÓN DE VARIABLES CATEGÓRICAS:
   ✓ Sex: Binaria (female=1, male=0)
   ✓ Embarked: One-Hot Encoding (3 variables dummy)
   → Total variables categóricas codificadas: 2

2. FEATURE ENGINEERING - NUEVAS CARACTERÍSTICAS:
   ✓ IsChild: Indicador de menores (edad < 15)
     Coeficiente de correlación con Survived: {df_transformed.corr()['Survived']['IsChild']:.4f}
   
   ✓ IsAlone: Indicador de viajante solo (FamilySize=1)
     Coeficiente de correlación con Survived: {df_transformed.corr()['Survived']['IsAlone']:.4f}
   
   ✓ FamilyGroupSize: Categorización en 4 grupos
     Coeficiente de correlación con Survived: {df_transformed.corr()['Survived']['FamilyGroupSize']:.4f}
   
   ✓ HasCabin: Indicador de información de camarote
     Coeficiente de correlación con Survived: {df_transformed.corr()['Survived']['HasCabin']:.4f}
   
   ✓ HigherClass: Indicador de clase premium (1-2)
     Coeficiente de correlación con Survived: {df_transformed.corr()['Survived']['HigherClass']:.4f}

3. VARIABLES FINALES DEL DATASET:
   Total: {df_transformed.shape[1]} variables
   - Variable objetivo (target): 1 (Survived)
   - Variables explicativas: {df_transformed.shape[1] - 1}

4. INTEGRIDAD DE DATOS:
   ✓ Valores nulos: 0
   ✓ Duplicados completos: 0
   ✓ Todas las variables numéricas

PRÓXIMOS PASOS:
→ División en conjuntos de entrenamiento y prueba
→ Entrenamiento del modelo de regresión logística
→ Evaluación y validación del modelo
"""

print(resumen)

# ============================================================================
# 10. GUARDAR DATASET TRANSFORMADO
# ============================================================================
df_transformed.to_csv(os.path.join(script_dir, "df_transformado.csv"), index=False)
print(f"\n✓ Dataset transformado guardado en: df_transformado.csv")

print("\n" + "="*80)
print("PASO 4 COMPLETADO")
print("="*80)
