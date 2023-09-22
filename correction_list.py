import pandas as pd
from itertools import zip_longest
from openpyxl import load_workbook
from google.oauth2 import service_account
from googleapiclient.discovery import build  # pip install google-api-python-client
from googleapiclient.http import MediaIoBaseUpload
import io

csv = pd.read_csv("resultado_test_main.csv")

lista_aprobados = []
lista_desaprobados = []

for index, row in csv.iterrows():

    usuario = row["Usuario"]
    cant_test = row["Cant_test"]
    aciertos = row["Aciertos"]

    if aciertos >= 5:

        lista_aprobados.append(usuario)

    elif aciertos < 5:

        lista_desaprobados.append(usuario)

# Creamos un DF a partir de las listas con las dos condiciones de los alumnos
condicion = {"Aprobados": lista_aprobados, "Desaprobados": lista_desaprobados}

df = pd.DataFrame(zip_longest(*condicion.values()), columns=condicion.keys())

# Guardamos el DF en un Excel
nombre_archivo = "lista_alumnos.xlsx"
df.to_excel(nombre_archivo, index=False)

# Cargar el archivo Excel y ajustar el ancho de las columnas
book = load_workbook(nombre_archivo)
writer = pd.ExcelWriter(nombre_archivo, engine="openpyxl")
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

# Obtener las dimensiones de las celdas de las dos columnas
dimensiones = {}
for columna in ["A", "B"]:
    sheet = writer.sheets["Sheet1"]
    columnas = sheet[columna]
    dimensiones[columna] = max(len(str(celda.value)) for celda in columnas)

# Ajustar el ancho de las columnas
for columna, ancho in dimensiones.items():
    writer.sheets["Sheet1"].column_dimensions[columna].width = ancho + 2

# Guardar los cambios en el archivo Excel
writer.save()

print(f"El DataFrame se ha guardado en el archivo {nombre_archivo}.")


credentials = service_account.Credentials.from_service_account_file("keys.json")

# Crea una instancia del cliente de la API de Google Drive
drive_service = build("drive", "v3", credentials=credentials)

# ID de la carpeta de destino en Google Drive
folder_id = "1VllVdNX9cjjY18VtzRNvjwHLjD_4A9Qd"

# Nombre del archivo en Google Drive
file_name = "lista_aprobados.xlsx"

# Ruta local del archivo Excel
local_file_path = "lista_alumnos.xlsx"

# Carga el archivo al contenido del archivo
file_content = None
with io.open(local_file_path, "rb") as file:
    file_content = file.read()

# Crea el cuerpo de la solicitud para subir el archivo
file_metadata = {"name": file_name, "parents": [folder_id]}
media = MediaIoBaseUpload(io.BytesIO(file_content), mimetype="application/vnd.ms-excel")

# Sube el archivo a Google Drive
uploaded_file = (
    drive_service.files()
    .create(body=file_metadata, media_body=media, fields="id")
    .execute()
)

# Obtiene el ID del archivo subido
file_id = uploaded_file["id"]
print("Archivo subido con éxito. ID del archivo: " + file_id)
