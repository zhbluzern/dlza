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
debug = 3 # adapt for debug mode. For prod: set to 99999 or bigger than the community record hits

def calculate_md5(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()

# read inventory file
with open(file_name, encoding="utf-8") as data_file:    
    data = json.load(data_file)
    for value in data:
        
        counter = counter+1

        # prepare object folder: make a directory for each object (SIP)  
        sip_folder = value["references"][-1][4:]
        #sip_folder = value["identifiers"][-1][4:]
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
            zenodo_link = f'{zenodo_api}/{zenodo_id}/files'    
            print(f"\n#{counter}: Get files from:",zenodo_link)
            response = requests.get(zenodo_link, params={'access_token': ACCESS_TOKEN})
            file_object = response.json()

            try: 
                for entry in file_object['entries']:
                    # get file info
                    download_url = entry['links']['content']
                    file_name = entry['key']
                    mimetype = entry['mimetype']
                    md5_checksum_zenodo = entry['checksum'][4:]

                    print("filename:",file_name, "mimetype:",mimetype)
                    local_file = f'{data_path}/{file_name}'
                    
                    # download content
                    response = requests.get(download_url, params={'access_token': ACCESS_TOKEN})
                    with open(local_file, mode="wb") as file:
                        file.write(response.content)
                        print(response)
                        print("Downloaded:",local_file)
                        # wait 1 second for every record so as not to overshoot zenodo rate limiting. 
                        time.sleep(1) 

                    # checksum comparison from local_file to md5_checksum
                    try:
                        md5_checksum = calculate_md5(local_file)
                        #print("MD5 Checksum local_file:", md5_checksum)
                        #print("MD5 checksum Zenodo-File:", md5_checksum_zenodo)
                        if md5_checksum == md5_checksum_zenodo:
                            print("Checksums match")
                        else:
                            print("checksums don't match!")        
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