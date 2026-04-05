import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def obtener_tasas_bcc():
    url = "https://www.bcc.gob.cu/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Intentamos obtener la web del Banco Central
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # El BCC pone las tasas en una tabla o divs. 
        # Buscamos los textos de USD y EUR.
        # Nota: Este scraping es sensible a cambios de diseño de la web.
        
        datos = {
            "fecha": datetime.now().strftime("%d/%m/%Y %I:%M %p"),
            "fuente": "Banco Central de Cuba",
            "usd": "480.00", # Valor por defecto si falla el scrape
            "eur": "554.16"
        }

        # Intentamos buscar los valores reales en el HTML (Segmento III)
        # Buscamos el texto que contiene "USD" y luego navegamos al valor
        items = soup.find_all('div')
        for i in range(len(items)):
            if "USD" in items[i].text and i+1 < len(items):
                # Lógica simplificada para encontrar el número
                texto = items[i].text.replace("USD", "").strip()
                if "." in texto:
                     datos["usd"] = texto[:6] # Tomamos los primeros caracteres del precio

        return datos
    except Exception as e:
        return {
            "fecha": datetime.now().strftime("%d/%m/%Y %I:%M %p"),
            "usd": "Error", 
            "error": str(e)
        }

if __name__ == "__main__":
    resultado = obtener_tasas_bcc()
    with open("cambio.json", "w") as f:
        json.dump(resultado, f, indent=4)
