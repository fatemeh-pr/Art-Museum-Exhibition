import os
import requests

GALLERIES = {
    "ancient": {
        "gallery_title": "Ancient Worlds",
        "query": "ancient Egyptian, Greek, Roman, archaeological artworks"
    },

    "portraits": {
        "gallery_title": "Portraits & People",
        "query": "portraits and depictions of people, historical figures, rulers, families and everyday people"
    },

    "nature": {
        "gallery_title": "Nature & Landscapes",
        "query": "landscapes, forests, mountains, gardens, rivers, oceans, flowers and scenes of nature"
    },

    "sacred": {
        "gallery_title": "Sacred & Mythological",
        "query": "religious, sacred and mythological art depicting gods, saints, biblical stories, legends and mythology"
    },

    "impressionism": {
        "gallery_title": "Impressionism & Beyond",
        "query": "impressionist, post-impressionist paintings, 19th and 20th century modern paintings, colorful light-filled"
    },

    "sculpture": {
        "gallery_title": "Sculpture",
        "query": "sculptures, statues, busts, reliefs and three-dimensional artworks"
    },

    "objects": {
        "gallery_title": "Art Beyond Paintings",
        "query": "decorative arts, textiles, furniture, ceramics, coins, jewelry and other historical objects"
    },

    "world": {
        "gallery_title": "Art Around the World",
        "query": "artworks from different cultures and regions around the world, showing diverse artistic traditions"
    }
}

API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise RuntimeError(
        "API_KEY environment variable is not set.\n"
        "Get an api-key by signing up in 'artsearch.io'"
    )


def get_artworks(gallery_name, number, offset):
    gallery = GALLERIES[gallery_name]
    headers = {
        "x-api-key": API_KEY,
    }
    params = {
        "query": gallery["query"],
        "number": number,
        "offset": offset
    }

    response = requests.get("https://api.artsearch.io/artworks",
                            params=params, 
                            headers=headers,
                            timeout=10)
    response.raise_for_status()
    data = response.json()
    artworks = data['artworks']
    counts = data['available']

    arts = []
    for artwork in artworks:
        art = {
            "id": artwork["id"],
            "title":artwork["title"],
            "image":artwork.get("image"),
        }
        arts.append(art)

    return gallery["gallery_title"], arts, counts


def get_random_art():
    headers = {
        "x-api-key": API_KEY,
        }

    response = requests.get("https://api.artsearch.io/artworks/random", 
                            headers=headers,
                            timeout=10)
    response.raise_for_status()
    data = response.json()

    random_art = {
        "id": data["id"], 
        "title": data["title"],
        "image": data["image"],
        "start_date": data.get("start_date", ""),
        "end_date": data.get("end_date", ""),
        "description": data.get("description", "")
    }
    return random_art


def get_art_info(art_id):
    headers = {
        "x-api-key": API_KEY,
        }

    response = requests.get(f"https://api.artsearch.io/artworks/{art_id}", 
                            headers=headers,
                            timeout=10)
    response.raise_for_status()
    data = response.json()

    artwork = {
        "id": data["id"], 
        "title": data["title"],
        "image": data["image"],
        "start_date": data.get("start_date", ""),
        "end_date": data.get("end_date", ""),
        "description": data.get("description", "")
    }
    return artwork
