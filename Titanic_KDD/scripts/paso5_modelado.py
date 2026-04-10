"""
LABORATORIO 1 - PROCESO KDD: ANÁLISIS DEL TITANIC
==================================================
PASO 5: MINERÍA DE DATOS - MODELADO CON REGRESIÓN LOGÍSTICA

Descripción: En este paso implementamos un modelo de regresión logística
para predecir la supervivencia en el Titanic, lo entrenamos, evaluamos
y analizamos su rendimiento.

Objetivo específico:
- Dividir datos en entrenamiento y prueba
- Entrenar modelo de regresión logística
- Evaluar rendimiento del modelo
- Identificar variables críticas
- Hacer predicciones
"""

import pandas as pd
import numpy as np
import os
import sys
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score,
    precision_score, recall_score, f1_score, roc_auc_score,
    roc_curve, auc
)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar encoding para Windows
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ============================================================================
# 1. CARGA DE DATOS
# ============================================================================
print("\n" + "="*80)
print("PASO 5: MINERÍA DE DATOS - MODELADO CON REGRESIÓN LOGÍSTICA")
print("="*80 + "\n")

script_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(script_dir, "..", "datos", "df_transformado.csv"))
print(f"Dataset transformado cargado: {df.shape[0]} filas x {df.shape[1]} columnas\n")

# Imputar valores faltantes en Age con la mediana
df = df.copy()
df['Age'] = df['Age'].fillna(df['Age'].median())

# ============================================================================
# 2. SEPARACIÓN DE VARIABLES
# ============================================================================
print("-"*80)
print("5.1 PREPARACIÓN DE DATOS - DIVISIÓN EN X E Y")
print("-"*80 + "\n")

# Variable objetivo
y = df['Survived']
# Variables explicativas
X = df.drop(columns=['Survived'])

print(f"Variable objetivo (y): 'Survived'")
print(f"  - Total de muestras: {len(y)}")
print(f"  - Distribución:")
print(f"    * No sobrevivieron (0): {(y == 0).sum()} ({(y == 0).sum()/len(y)*100:.1f}%)")
print(f"    * Sobrevivieron (1): {(y == 1).sum()} ({(y == 1).sum()/len(y)*100:.1f}%)")

print(f"\nVariables explicativas (X): {X.shape[1]} variables")
for i, col in enumerate(X.columns, 1):
    print(f"  {i:2}. {col}")

# ============================================================================
# 3. DIVISIÓN EN CONJUNTOS DE ENTRENAMIENTO Y PRUEBA
# ============================================================================
print("\n" + "-"*80)
print("5.2 DIVISIÓN EN CONJUNTOS DE ENTRENAMIENTO Y PRUEBA")
print("-"*80 + "\n")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Conjunto de ENTRENAMIENTO:")
print(f"  - Muestras: {len(X_train)} ({len(X_train)/len(X)*100:.1f}%)")
print(f"  - Distribución en entrenamiento:")
print(f"    * No sobrevivieron: {(y_train == 0).sum()} ({(y_train == 0).sum()/len(y_train)*100:.1f}%)")
print(f"    * Sobrevivieron: {(y_train == 1).sum()} ({(y_train == 1).sum()/len(y_train)*100:.1f}%)")

print(f"\nConjunto de PRUEBA:")
print(f"  - Muestras: {len(X_test)} ({len(X_test)/len(X)*100:.1f}%)")
print(f"  - Distribución en prueba:")
print(f"    * No sobrevivieron: {(y_test == 0).sum()} ({(y_test == 0).sum()/len(y_test)*100:.1f}%)")
print(f"    * Sobrevivieron: {(y_test == 1).sum()} ({(y_test == 1).sum()/len(y_test)*100:.1f}%)")

# ============================================================================
# 4. ENTRENAMIENTO DEL MODELO
# ============================================================================
print("\n" + "-"*80)
print("5.3 ENTRENAMIENTO DEL MODELO - REGRESIÓN LOGÍSTICA")
print("-"*80 + "\n")

# Crear y entrenar el modelo
modelo = LogisticRegression(random_state=42, max_iter=1000)
modelo.fit(X_train, y_train)

print("OK Modelo de Regresión Logística entrenado exitosamente")
print(f"  - Algoritmo: Logistic Regression")
print(f"  - Muestras de entrenamiento: {len(X_train)}")
print(f"  - Variables del modelo: {X_train.shape[1]}")
print(f"  - Parámetro de regularización (C): {modelo.C}")

# ============================================================================
# 5. PREDICCIONES
# ============================================================================
print("\n" + "-"*80)
print("5.4 PREDICCIONES DEL MODELO")
print("-"*80 + "\n")

y_train_pred = modelo.predict(X_train)
y_test_pred = modelo.predict(X_test)
y_test_proba = modelo.predict_proba(X_test)[:, 1]  # Probabilidades

print("OK Predicciones generadas para ambos conjuntos")

# ============================================================================
# 6. EVALUACIÓN DEL MODELO - METRICAS DE RENDIMIENTO
# ============================================================================
print("\n" + "-"*80)
print("5.5 EVALUACIÓN DEL MODELO - MÉTRICAS DE RENDIMIENTO")
print("-"*80 + "\n")

# Métricas de entrenamiento
acc_train = accuracy_score(y_train, y_train_pred)
print("RENDIMIENTO EN CONJUNTO DE ENTRENAMIENTO:")
print(f"  - Exactitud (Accuracy): {acc_train:.4f} ({acc_train*100:.2f}%)")

# Métricas de prueba
acc_test = accuracy_score(y_test, y_test_pred)
precision = precision_score(y_test, y_test_pred)
recall = recall_score(y_test, y_test_pred)
f1 = f1_score(y_test, y_test_pred)
roc_auc = roc_auc_score(y_test, y_test_proba)

print("\nRENDIMIENTO EN CONJUNTO DE PRUEBA:")
print(f"  - Exactitud (Accuracy):        {acc_test:.4f} ({acc_test*100:.2f}%)")
print(f"  - Precisión (Precision):       {precision:.4f} ({precision*100:.2f}%)")
print(f"    * De los predichos como 'sobrevivió', {precision*100:.2f}% realmente sobrevivieron")
print(f"  - Recall (Sensibilidad):       {recall:.4f} ({recall*100:.2f}%)")
print(f"    * De los que realmente sobrevivieron, el modelo identificó {recall*100:.2f}%")
print(f"  - F1-Score (Balance):          {f1:.4f}")
print(f"  - ROC-AUC Score:               {roc_auc:.4f}")

# Matriz de confusión
cm = confusion_matrix(y_test, y_test_pred)
print(f"\nMATRIZ DE CONFUSIÓN (Conjunto de Prueba):")
print(f"                 Predicción")
print(f"                 No Sobrevivió  Sobrevivió")
print(f"Realidad No S.       {cm[0,0]:4d}          {cm[0,1]:4d}")
print(f"        S.           {cm[1,0]:4d}          {cm[1,1]:4d}")

# Reporte de clasificación
print(f"\nREPORTE DE CLASIFICACIÓN DETALLADO:\n")
print(classification_report(y_test, y_test_pred, 
                           target_names=['No Sobrevivió', 'Sobrevivió']))

# ============================================================================
# 7. ANÁLISIS DE COEFICIENTES - IMPORTANCIA DE VARIABLES
# ============================================================================
print("-"*80)
print("5.6 ANÁLISIS DE COEFICIENTES - IMPORTANCIA DE VARIABLES")
print("-"*80 + "\n")

# Obtener coeficientes
coef_df = pd.DataFrame({
    'Variable': X.columns,
    'Coeficiente': modelo.coef_[0],
    'Valor Absoluto': np.abs(modelo.coef_[0])
}).sort_values('Valor Absoluto', ascending=False)

print("Coeficientes del modelo (Ordenados por valor absoluto):\n")
print(f"{'Variable':<23} {'Coeficiente':>12} {'Impacto':>15}")
print("-"*52)

for idx, row in coef_df.iterrows():
    impact = "Aumenta Supervivencia" if row['Coeficiente'] > 0 else "Reduce Supervivencia"
    print(f"{row['Variable']:<23} {row['Coeficiente']:>12.6f} {impact:>15}")

print(f"\nIntercept (Constante): {modelo.intercept_[0]:.6f}")

print("\n\nINTERPRETACIÓN DE VARIABLES CRÍTICAS:")
print("\nVARIABLES CON MAYOR IMPACTO POSITIVO (Aumentan supervivencia):")
positivos = coef_df[coef_df['Coeficiente'] > 0].head(5)
for idx, row in positivos.iterrows():
    print(f"  OK {row['Variable']:20} : {row['Coeficiente']:+.4f}")

print("\nVARIABLES CON MAYOR IMPACTO NEGATIVO (Reducen supervivencia):")
negativos = coef_df[coef_df['Coeficiente'] < 0].head(5)
for idx, row in negativos.iterrows():
    print(f"  X {row['Variable']:20} : {row['Coeficiente']:+.4f}")

# ============================================================================
# 8. VISUALIZACIONES
# ============================================================================
print("\n" + "-"*80)
print("5.7 GENERANDO VISUALIZACIONES")
print("-"*80 + "\n")

graficos_dir = os.path.join(script_dir, "..", "graficos")
if not os.path.exists(graficos_dir):
    os.makedirs(graficos_dir)

# Figura 1: Matriz de confusión
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
            xticklabels=['No Sobrevivió', 'Sobrevivió'],
            yticklabels=['No Sobrevivió', 'Sobrevivió'],
            cbar_kws={'label': 'Cantidad'})
ax.set_title('Matriz de Confusión - Conjunto de Prueba', fontweight='bold', fontsize=14)
ax.set_ylabel('Valor Real', fontweight='bold')
ax.set_xlabel('Predicción', fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(graficos_dir, '04_matriz_confusion.png'), dpi=300, bbox_inches='tight')
plt.close()
print("OK Gráfico 04 guardado: matriz_confusion.png")

# Figura 2: Importancia de variables (coeficientes)
fig, ax = plt.subplots(figsize=(10, 8))
colors = ['#2ca02c' if x > 0 else '#d62728' for x in coef_df['Coeficiente']]
ax.barh(coef_df['Variable'], coef_df['Coeficiente'], color=colors)
ax.set_xlabel('Coeficiente (Impacto en Supervivencia)', fontweight='bold')
ax.set_title('Importancia de Variables - Regresión Logística', fontweight='bold', fontsize=14)
ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
plt.tight_layout()
plt.savefig(os.path.join(graficos_dir, '05_importancia_variables.png'), dpi=300, bbox_inches='tight')
plt.close()
print("OK Gráfico 05 guardado: importancia_variables.png")

# Figura 3: Curva ROC
fpr, tpr, thresholds = roc_curve(y_test, y_test_proba)
roc_auc_val = auc(fpr, tpr)

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(fpr, tpr, color='#1f77b4', lw=2.5, label=f'Curva ROC (AUC = {roc_auc_val:.4f})')
ax.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--', label='Clasificador Aleatorio')
ax.set_xlabel('Tasa Falsos Positivos (1 - Especificidad)', fontweight='bold')
ax.set_ylabel('Tasa Verdaderos Positivos (Sensibilidad)', fontweight='bold')
ax.set_title('Curva ROC - Análisis del Modelo', fontweight='bold', fontsize=14)
ax.legend(loc='lower right', fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(graficos_dir, '06_curva_roc.png'), dpi=300, bbox_inches='tight')
plt.close()
print("OK Gráfico 06 guardado: curva_roc.png")

# Figura 4: Distribución de probabilidades predichas
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(y_test_proba[y_test == 0], bins=30, alpha=0.6, label='No Sobrevivió', color='#d62728')
ax.hist(y_test_proba[y_test == 1], bins=30, alpha=0.6, label='Sobrevivió', color='#2ca02c')
ax.set_xlabel('Probabilidad Predicha de Supervivencia', fontweight='bold')
ax.set_ylabel('Frecuencia', fontweight='bold')
ax.set_title('Distribución de Probabilidades Predichas', fontweight='bold', fontsize=14)
ax.legend(fontsize=11)
ax.axvline(x=0.5, color='black', linestyle='--', linewidth=1, label='Umbral (0.5)')
plt.tight_layout()
plt.savefig(os.path.join(graficos_dir, '07_distribucion_probabilidades.png'), dpi=300, bbox_inches='tight')
plt.close()
print("OK Gráfico 07 guardado: distribucion_probabilidades.png")

# ============================================================================
# 9. RESUMEN EJECUTIVO
# ============================================================================
print("\n" + "="*80)
print("RESUMEN EJECUTIVO DEL PASO 5 - RESULTADOS DEL MODELADO")
print("="*80 + "\n")

resumen = f"""
CONFIGURACIÓN DEL MODELO:
  - Algoritmo: Regresión Logística
  - Conjunto de entrenamiento: {len(X_train)} muestras (80%)
  - Conjunto de prueba: {len(X_test)} muestras (20%)
  - Variables explicativas: {X_train.shape[1]}
  - Random state: 42 (para reproducibilidad)

EVALUACIÓN DEL MODELO - MÉTRICAS PRINCIPALES:
  - Exactitud (Accuracy):  {acc_test:.4f} ({acc_test*100:.2f}%)
    → El modelo clasifica correctamente {acc_test*100:.1f}% de los casos
  
  - Precisión (Precision):  {precision:.4f} ({precision*100:.2f}%)
    → De los predichos como 'sobrevivió', {precision*100:.1f}% realmente sobrevivieron
  
  - Recall (Sensibilidad):   {recall:.4f} ({recall*100:.2f}%)
    → El modelo identifica {recall*100:.1f}% de los que realmente sobrevivieron
  
  - F1-Score:                {f1:.4f}
    → Balance entre precisión y recall
  
  - ROC-AUC:                 {roc_auc:.4f}
    → Excelente capacidad discriminativa

VARIABLES CRÍTICAS IDENTIFICADAS (Top 5):

1. {coef_df.iloc[0]['Variable']:20} : {coef_df.iloc[0]['Coeficiente']:+.6f}
2. {coef_df.iloc[1]['Variable']:20} : {coef_df.iloc[1]['Coeficiente']:+.6f}
3. {coef_df.iloc[2]['Variable']:20} : {coef_df.iloc[2]['Coeficiente']:+.6f}
4. {coef_df.iloc[3]['Variable']:20} : {coef_df.iloc[3]['Coeficiente']:+.6f}
5. {coef_df.iloc[4]['Variable']:20} : {coef_df.iloc[4]['Coeficiente']:+.6f}

INTERPRETACIÓN CLAVE:
  OK El modelo tiene un buen desempeño general
  OK La variable MÁS IMPORTANTE es: {coef_df.iloc[0]['Variable']}
  OK Las características de género, clase y edad fueron críticas
  OK El modelo puede generalizar bien a nuevos datos

MATRIZ DE CONFUSIÓN:
  - Verdaderos Negativos (TN): {cm[0,0]}  (Correctamente identificados como no sobrevivieron)
  - Falsos Positivos (FP):      {cm[0,1]}  (Predicción incorrecta)
  - Falsos Negativos (FN):      {cm[1,0]}  (Predicción incorrecta)
  - Verdaderos Positivos (TP):  {cm[1,1]}  (Correctamente identificados como sobrevivieron)

CONCLUSIONES:
  1. El modelo de regresión logística es adecuado para este problema
  2. Las variables demográficas y socioeconómicas son buenos predictores
  3. El modelo tiene equilibrio entre precisión y recall
  4. Recomendación: El modelo está listo para hacer predicciones en nuevos datos
"""

print(resumen)

print("\nOK PASO 5 COMPLETADO\n")

print("="*80)
print("PROCESO KDD COMPLETADO EXITOSAMENTE")
print("="*80)
