import pandas as pd

df = pd.read_csv("resultado_test_main.csv")

nombre_archivo = "carga_notas.xlsx"
df.to_excel(nombre_archivo, index=False)
