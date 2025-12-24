import os
import json
import requests
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pathlib import Path
from dotenv import load_dotenv

# FASE 4: Consumo de la Marvel API
BASE_DIR = Path(__file__).resolve().parents[1] 
load_dotenv(BASE_DIR / ".env")
BASE_URL = "https://www.superheroapi.com/api.php"
TOKEN = os.getenv("SUPERHERO_API_TOKEN") 


def api_get(hero_path, timeout: int = 10) -> dict:
    """Llama a SuperHero API y devuelve el JSON como dict."""
    if not TOKEN:
        raise RuntimeError("No encuentro SUPERHERO_API_TOKEN. ")

    url = f"{BASE_URL}/{TOKEN}/{hero_path}"
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        data = r.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error de red/HTTP llamando a {url}: {e}")
    except ValueError:
        raise RuntimeError(f"La API no devolvió JSON válido: {url}")

    # La API suele devolver "response": "success" o "error"
    if data.get("response") == "error":
        raise RuntimeError(f"Error API: {data.get('error', 'unknown error')}")

    return data


def obtener_personaje_api_por_id(hero_id: int) -> dict:
    # Endpoint típico: /{id} :contentReference[oaicite:0]{index=0}
    return api_get(str(hero_id))


def obtener_personajes_api(ids: list[int]) -> list[dict]:
    """
    Trae 5 personajes por ID.
    Si alguno falla, lo salta (pero te avisa).
    """
    personajes = []
    for hero_id in ids:
        try:
            personajes.append(obtener_personaje_api_por_id(hero_id))
        except Exception as e:
            print(f"[WARN] No pude traer id={hero_id}: {e}")
    return personajes

# FASE 1: Lectura del archivo local JSON
def obtener_personajes_local(ruta_json: str = "superheros.json") -> list[dict]:
    with open(ruta_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data["results"][0:5]

# Obtenemos 5 personajes de la API y otros 5 del archivo local
personajes_local = obtener_personajes_local()
personajes_api = [obtener_personaje_api_por_id(i) for i in range(1, 6)]

# Eliminar duplicados basándonos en el ID
personajes_unicos = []
ids_vistos = set()
for p in personajes_api + personajes_local:
    pid = str(p.get("id"))
    if pid not in ids_vistos:
        ids_vistos.add(pid)
        personajes_unicos.append(p)

# FASE 2: Trabajo con datos
personajes_filtrados = []

for personaje in personajes_unicos:
    personajes_filtrados.append({
        'id': personaje['id'],
        'name': personaje['name'],
        'intelligence': personaje['powerstats']['intelligence'],
        'strength': personaje['powerstats']['strength'],
        'speed': personaje['powerstats']['speed']
    })

def busqueda_personaje(personajes):
    ''' función en la que se devuelve un personaje que pida el usuario a partir del nombre'''

    nombre_personaje = input('¿De qué personaje quieres conocer sus estadísticas y generar una imagen? ')

    for personaje in personajes:
        if personaje["name"] == nombre_personaje:
            return personaje

    print(f'El personaje {nombre_personaje} no se encuentra en la lista')
    return False

# FASE 3: Gráficas
def graf_estadisticas_personaje(personaje):
    ''' Función que devuelve una gráfica de barras mostrando las estadísticas de un personaje indicado por el usuario'''    

    stats = ["intelligence", "strength", "speed"]
    valores = [int(personaje[s]) for s in stats]

    f = plt.figure(figsize=(12,8))

    # Histograma
    ax1 = f.add_subplot(1,2,1)
    ax1.bar(stats, valores, color=['g', 'r', 'b'])
    ax1.set_title(f"Estadísticas de {personaje['name']}")
    ax1.set_ylabel('Valor')
    ax1.set_xlabel('Powerstats')
    ax1.set_ylim([0,100])
    # Gráfica circular
    ax2 = f.add_subplot(1,2,2)
    ax2.pie(valores, labels=stats, colors=['g', 'r', 'b'], autopct='%1.1f%%')
    ax2.set_title(f"Estadísticas de {personaje['name']}")
    plt.show()

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=valores + [valores[0]],
        theta=stats + [stats[0]],
        mode="lines+markers+text",
        text=[str(v) for v in valores] + [str(valores[0])],
        textposition="top center",
        fill='toself',
        name=personaje["name"]
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title=f"Perfil de {personaje['name']}"
    )

    fig.show()

# FASE OPCIONAL: Uso de Dall-e

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise RuntimeError("No encuentro OPENAI_API_KEY.")

endpoint_IEBS = os.getenv("endpoint_IEBS")
if not endpoint_IEBS:
    raise RuntimeError("No encuentro endpoint_IEBS.")

# Debug: mostrar que las variables se cargaron
print(f"✓ OPENAI_API_KEY cargada: {OPENAI_KEY[:10]}..." if OPENAI_KEY else "✗ OPENAI_API_KEY no encontrada")
print(f"✓ endpoint_IEBS cargado: {endpoint_IEBS}")

def generar_imagen_openai(hero:str):
    ''' Función que genera una imagen a partir del nombre de un superhéroe usando Dall-e'''

    try:
        prompt = f"Creame un personaje similar en cuanto a aspecto a {hero} pero que no tenga problemas de filtro de contenidos"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENAI_KEY}',
        }
        payload = {
            "model": "dall-e-3",
            "prompt" : f"{prompt}",
            "size" : "1024x1024",
            "style" : "vivid",
            "quality" : "standard",
            "n" : 1
        }

        response = requests.post(endpoint_IEBS, headers=headers, json=payload)

        if response.status_code == 200:
            image_url = response.json()['data'][0]['url']
            print(f'Imagen generada para {hero}: {image_url}')

            # Descargar la imagen
            img_resp = requests.get(image_url, timeout=60)
            img_resp.raise_for_status()

            # Nombre de archivo seguro
            safe_name = "".join(c for c in hero if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
            filepath = os.path.join(os.getcwd(), f"{safe_name}.png")  # directorio actual

            # Guardar en el directorio actual
            with open(filepath, "wb") as f:
                f.write(img_resp.content)
            print(f'Imagen guardada en: {filepath}')
        else:
            print(f'Error al generar la imagen: {response.status_code}, {response.text}')
    except Exception as e:
        print(f'Error en generar_imagen_openai: {e}')


if __name__ == "__main__":

    print('Los personajes que se tienen en cartera son:')
    for personaje in personajes_filtrados:
        print(f'''Personaje {personaje['id']}, llamado {personaje['name']}, tiene una inteligencia de {personaje['intelligence']}, 
          una fuerza de {personaje['strength']} y una velocidad de {personaje['speed']}''')
    
    personaje = False
    while not personaje:
        personaje = busqueda_personaje(personajes_filtrados)
        if personaje:
            graf_estadisticas_personaje(personaje)
            generar_imagen_openai(personaje['name'])
