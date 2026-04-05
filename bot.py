import requests
import json
from datetime import datetime

def obtener_datos():
    # Nota: Aquí pondrías la lógica de scraping. 
    # Para el ejemplo, usaremos datos fijos o una búsqueda simple.
    # El Toque a veces requiere headers para no bloquearte.
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Ejemplo: Supongamos que sacamos los datos de una API o scraping
    # Por ahora, simulamos el resultado:
    datos = {
        "fecha": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
        "usd": 325, # Aquí iría la lógica de extracción real
        "eur": 335,
        "cup": 1
    }
    return datos

if __name__ == "__main__":
    resultado = obtener_datos()
    with open("cambio.json", "w") as f:
        json.dump(resultado, f, indent=4)
