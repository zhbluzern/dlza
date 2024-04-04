import fitz  # PyMuPDF
import requests
import json
import os
import time
import config
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# get access token
load_dotenv()
ACCESS_TOKEN = os.getenv('access_token')

# get config variables
file_name = config.inventory_file
community = config.collection_id
objects_path = f'{config.user_root}/{config.collection_id}/{config.object_path}'
zenodo_api = config.zenodo_api

download_manually = f'{community}_download_manually.txt'
counter = 0
debug = 20 # adapt for debug mode. For prod: set to 99999

# read inventory file
with open(file_name, encoding="utf-8") as data_file:    
    data = json.load(data_file)
    for value in data:
        
        counter = counter+1
        
        if counter <= debug: 
    
            # prepare object folder: make a directory for each object (SIP)  
            foldername = value["references"][1]
            sip_path = f"{objects_path}/{foldername}"                  
            Path(f'{sip_path}').mkdir(parents=True, exist_ok=True)
            
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

                    print("filename:",file_name, "mimetype:",mimetype)
                    local_file = f'{sip_path}/{file_name}'
                    
                    # download content
                    response = requests.get(download_url, params={'access_token': ACCESS_TOKEN})
                    with open(local_file, mode="wb") as file:
                        file.write(response.content)
                        print(response)
                        print("Downloaded:",local_file)
                        # wait 1 second for every record so as not to overshoot zenodo rate limiting. 
                        time.sleep(1) 

                    # distinguish between pdf files and other files
                    if mimetype == 'application/pdf':
                        # check some stuff on file's integrity, e.g. count pages
                        try:
                            with fitz.open(local_file) as pdf_document:
                                if pdf_document.page_count != 0:
                                    print("PDF page count:",pdf_document.page_count)
                        except Exception as e:
                            print(f"---   Error checking PDF file {file_name}: {e}")
                            # append download url to download_manually.txt
                            with open(download_manually, 'a') as file:
                                file.write(download_url)
                                file.write("\n")
                                print(f"URL {download_url} appended to {download_manually}\n")                                
                        
                    else:
                        print("---   Not a PDF")
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