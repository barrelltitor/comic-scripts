import requests
import sys

MYLAR_API_KEY = "iAmASuperSecretApiKey"
MYLAR_API_URL = "http://192.168.88.209:4005/api"

def get_comic(comic_id):
    get_url = f"{api_url}?apikey={apikey}&cmd=getComic&id={comic_id}"
    response = requests.get(get_url)
    if response.status_code == 200:
        data = response.json()
        if data['data']['comic']:
            return data['data']['comic'][0]['id']
    return None

def add_comic(comic_id):
    add_url = f"{api_url}?apikey={apikey}&cmd=addComic&id={comic_id}"
    response = requests.get(add_url)
    return response.status_code

def main(comic_id):
    existing_comic_id = get_comic(comic_id)
    if existing_comic_id != comic_id:
        status_code = add_comic(comic_id)
        if status_code == 200:
            print(f"Comic ID {comic_id} added successfully.")
        else:
            print(f"Failed to add Comic ID {comic_id}. Status code: {status_code}")
    else:
        print(f"{comic_id} - already exists")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <comic_id>")
        sys.exit(1)
    comic_id = sys.argv[1]
    main(comic_id)