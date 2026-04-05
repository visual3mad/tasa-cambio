import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def obtener_datos():
    # Valores de respaldo basados en tu captura (por si la web falla)
    datos = {
        "fecha": datetime.now().strftime("%d/%m/%Y %I:%M %p"),
        "oficial": {"usd": "480.00", "eur": "554.16"},
        "informal": {"usd": "520.00", "eur": "590.00"} # Actualizado a tu captura
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1'
    }

    try:
        # Intentamos entrar a El Toque
        url = "https://eltoque.com/"
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscamos las etiquetas que contienen los precios
            # El Toque usa clases como 'price-text' o dentro de tablas específicas
            indices = soup.find_all('span', class_='price-text')
            
            # Si encontramos datos, los extraemos con cuidado
            if len(indices) >= 2:
                # Limpiamos el texto para quedarnos solo con el número
                usd_val = indices[0].text.replace('CUP', '').strip()
                eur_val = indices[1].text.replace('CUP', '').strip()
                
                # Validamos que sean números lógicos (ej. mayores a 100)
                if float(usd_val.replace(',','')) > 100:
                    datos["informal"]["usd"] = usd_val
                if float(eur_val.replace(',','')) > 100:
                    datos["informal"]["eur"] = eur_val
    except Exception as e:
        print(f"Error: {e}")

    return datos

if __name__ == "__main__":
    resultado = obtener_datos()
    with open("cambio.json", "w") as f:
        json.dump(resultado, f, indent=4)
