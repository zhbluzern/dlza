#import fitz  # PyMuPDF
import requests
import json
import os
import time
import config
import hashlib
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# get access token
load_dotenv()
ACCESS_TOKEN = os.getenv('access_token')

# get config variables
localdrive = config.user_root
org_id = config.organisation_id
collection = config.collection_id

file_name = f'{collection}/{collection}_inventory.json'
community = config.collection_id
zenodo_api = config.baseurl_zenodo_api

download_manually = f'{community}_download_manually.txt'
counter = 0
debug = 9999 # adapt for debug mode. For prod: set to 99999 or bigger than the community record hits

def calculate_md5(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()


def shorten_filename(filename, max_len=120):
    name, ext = os.path.splitext(filename)
    if len(filename) <= max_len:
        return filename

    # Hash aus Originalnamen (eindeutig!)
    h = hashlib.sha1(filename.encode("utf-8")).hexdigest()[:10]
    return f"{name[:40]}_{h}{ext}"


# check for already processed files
processed_file = f'{community}_processed.txt'
if os.path.exists(processed_file):
    with open(processed_file, 'r') as f:
        processed_ids = set(line.strip() for line in f)
else:
    processed_ids = set()

# read inventory file
with open(file_name, encoding="utf-8") as data_file:    
    data = json.load(data_file)
    for value in data:
        
        counter = counter+1

        # prepare object folder: make a directory for each object (SIP)  
        sip_folder = value["references"][-1][4:]
        data_path = f'{localdrive}/{collection}/{sip_folder}/data/'
        Path(f'{data_path}').mkdir(parents=True, exist_ok=True)

        # check if debug mode, only download test files        
        if counter <= debug: 
            
            # get the necessary identifier
            identifiers = {}
            for item in value["identifiers"]:
                # split identifiers in dict
                [key, value] = item.split(':',1)
                identifiers[key] = value

            # get the file download link from zenodo: 
            zenodo_id = identifiers['zenodo'] 
            # Fortschritt prüfen
            if zenodo_id in processed_ids:
                print(f"Skipping already processed: {zenodo_id}")
                continue

            zenodo_link = f'{zenodo_api}/{zenodo_id}/files'    
            print(f"\n#{counter}: Get files from:",zenodo_link)
            response = requests.get(zenodo_link, params={'access_token': ACCESS_TOKEN})
            #file_object = response.json()
            if response.status_code == 200 and response.headers.get('Content-Type', '').startswith('application/json'):
                file_object = response.json()
            else:
                print(f"---   Error: Status {response.status_code}, Content-Type: {response.headers.get('Content-Type')}")
                print(f"---   Response text: {response.text[:200]}")  # Nur die ersten 200 Zeichen anzeigen
                with open(download_manually, 'a') as file:
                    file.write(zenodo_link)
                    file.write("\n")
                continue

            try: 
                for entry in file_object['entries']:
                    # get file info
                    download_url = entry['links']['content']
                    file_name = entry['key']
                    mimetype = entry['mimetype']
                    md5_checksum_zenodo = entry['checksum'][4:]

                    print("filename:",file_name, "mimetype:",mimetype)
                    safe_filename = shorten_filename(file_name)
                    print(safe_filename)

                    local_file = f'{data_path}/{safe_filename}'
                    
                    # download content
                    #response = requests.get(download_url, params={'access_token': ACCESS_TOKEN})
                    
                    with requests.get(download_url, params={'access_token': ACCESS_TOKEN}, stream=True) as response:
                        response.raise_for_status()  # Fehlerbehandlung
                        with open(local_file, 'wb') as f:  
                            try:                         
                                for chunk in response.iter_content(chunk_size=8192):  # 8KB pro Chunk
                                    if chunk:  # Filter leere Chunks
                                        f.write(chunk)
                                print(response.status_code,"- Downloaded:",local_file)
                            except Exception as e:
                                print(f"---   Error downloading file {local_file}: {e}")
                                # append download url to download_manually.txt
                                with open(download_manually, 'a') as file:
                                    file.write(download_url)
                                    file.write("\n")
                                    print(f"URL {download_url} appended to {download_manually}, download problems.\n")

                    # wait 1 second for every record so as not to overshoot zenodo rate limiting.
                    time.sleep(1) 

                    # checksum comparison from local_file to md5_checksum
                    try:
                        md5_checksum = calculate_md5(local_file)

                        if md5_checksum == md5_checksum_zenodo:
                            print("Checksums match")
                            # Fortschritt speichern
                            with open(processed_file, 'a') as pf:
                                pf.write(f"{zenodo_id}\n")
                        else:
                            print("---------------------------------------------------------------------------------- Checksums don't match!")        
                            # append download url to download_manually.txt
                            with open(download_manually, 'a') as file:
                                file.write(download_url)
                                file.write("\n")
                                print(f"URL {download_url} appended to {download_manually}\n")                             

                    except Exception as e:
                        print(f"---   Error checking file checksum {local_file}: {e}")
                        # append download url to download_manually.txt
                        with open(download_manually, 'a') as file:
                            file.write(download_url)
                            file.write("\n")
                            print(f"URL {download_url} appended to {download_manually}\n")                                
                        
            except KeyError:
                print("---   KeyError: files not found, download manually:")
                # append download url to download_manually.txt
                with open(download_manually, 'a') as file:
                    file.write(zenodo_link)
                    file.write("\n")
                    print(f"URL {zenodo_link} appended to {download_manually}\n")
        
print("\nFinished at ",datetime.today().strftime('%Y-%m-%d %H:%M:%S'))