import os
import zipfile
import requests
import re
import argparse

MYLAR_API_KEY = "694633e472e8b4305b02243b2b203d63"
MYLAR_API_URL = "http://192.168.88.209:4005/api"
COMIC_VINE_API_URL = "https://cvcache.titor.dev/api"
COMIC_VINE_API_KEY = "" # Add this to use your own api key, otherwise uses the Titor cache
# Extract Issue ID from ComicInfo.xml
def extract_issue_id(cbz_file):
    with zipfile.ZipFile(cbz_file, 'r') as zip_ref:
        if 'ComicInfo.xml' in zip_ref.namelist():
            with zip_ref.open('ComicInfo.xml') as file:
                content = file.read().decode('utf-8')
                match = re.search(r'Issue ID (\d+)', content)
                if match:
                    return match.group(1)
        else:
            print(f"ComicInfo.xml not found in {cbz_file}")
    return None

# Get series ID from Issue ID
def get_series_id(issue_id):
    if COMIC_VINE_API_KEY:
        url = f"{COMIC_VINE_API_URL}/issue/4000-{issue_id}?format=json?api_key={COMIC_VINE_API_KEY}"
    else:
        url = f"{COMIC_VINE_API_URL}/issue/4000-{issue_id}?format=json" # Uses the Titor Cache, no rate limit right now, but pls don't abuse. If we hit the CV rate limit, we'll have to wait and try again, or add your own comicvine key
    response = requests.get(url, headers={"x-titor-key": "a782f254-341f-49cb-bada-6d6343652d5c"}) # We send it to comicvine too as a header, but it shouldn't matter
    if response.status_code == 200:
        data = response.json()
        return data.get('results', {}).get('volume', {}).get('id')
    elif response.status_code == 420:
        raise Exception("I reached my rate limit on all my keys, or my cache is down for whatever reason. Please wait and try again, or add your own api key.")
    return None


def mylar_get_comic(comic_id):
    get_url = f"{MYLAR_API_URL}?apikey={MYLAR_API_KEY}&cmd=getComic&id={comic_id}"
    response = requests.get(get_url)
    if response.status_code == 200:
        data = response.json()
        if data['data']['comic']:
            return data['data']['comic'][0]['id']
    return None

def mylar_add_comic(comic_id):
    add_url = f"{MYLAR_API_URL}?apikey={MYLAR_API_KEY}&cmd=addComic&id={comic_id}"
    response = requests.get(add_url)
    return response.status_code

def add_to_mylar(comics):
    for comic_id in comics:
        existing_comic_id = mylar_get_comic(comic_id)
        if existing_comic_id != comic_id:
            status_code = mylar_add_comic(comic_id)
            if status_code == 200:
                print(f"Comic ID {comic_id} added successfully.")
            else:
                print(f"Failed to add Comic ID {comic_id}. Status code: {status_code}")
        else:
            print(f"{comic_id} - already exists")


def main():
    parser = argparse.ArgumentParser(description='Process comic files.')
    parser.add_argument('--folder-per-series', action='store_true', help='Only check one comic issue per folder')
    parser.add_argument('--one-series-per-name', action='store_true', help='Only process one comic issue per series name')
    args = parser.parse_args()

    comics = set()
    processed_series = set()
    # Find all .cbz files and process each one
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".cbz"):
                series_name = re.match(r'^(.*?) \d+ \(\d{4}\)\.cbz$', file)
                if series_name:
                    series_name = series_name.group(1)
                    if args.one_series_per_name:
                        if series_name in processed_series:
                            continue # Only process one comic issue per series name
                        print(series_name)
                        processed_series.add(series_name)
                cbz_file = os.path.join(root, file)
                print(f"Processing file: {cbz_file}")
                issue_id = extract_issue_id(cbz_file)
                if issue_id:
                    print(f"Found Issue ID: {issue_id}")
                    series_id = get_series_id(issue_id)
                    if series_id:
                        print(f"Found Series ID: {series_id}")
                        comics.add(series_id)
            if args.folder_per_series:
                break # Only check one comic issue per folder
            
    add_to_mylar(comics)

if __name__ == "__main__":
    main()
