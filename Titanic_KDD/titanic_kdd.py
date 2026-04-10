import pandas as pd
import os

# Obtener la ruta de la carpeta actual del script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Cargar archivo Titanic (ruta relativa al script)
csv_path = os.path.join(script_dir, "train.csv")
df = pd.read_csv(csv_path)

# Mostrar primeras 5 filas
print(df.head())