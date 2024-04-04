import requests
import json
from datetime import datetime
from pathlib import Path
from sickle import Sickle
import config
import time


# which metadata is available:
marc = config.marcxml
marc_url = config.marcxml_baseurl

datacite = config.datacite
dublincore = config.dc
apidata = config.apidata
zenodo_url = config.zenodo_baseurl
zenodo_api = config.zenodo_api

tei = config.tei
ecodices_url = config.ecodices_url

# general config:

urn = config.ingest_workflow
collection = config.collection_id

md_path = f'{collection}/{config.metadata_path}'
org_id = config.organisation_id

input_file = f'{config.inventory_file}'
counter = 0
debug = 99 # debug mode. How many records are harvested. Enter 9999 for production mode.


with open(input_file, encoding="utf-8", errors="replace") as data_file:    
    data = json.load(data_file)
    for value in data:
        
        counter+= 1 
        
        if counter<= debug: 

            # create new directory for each signature (ignore, if it already exists)            
            foldername = value["references"][-1]
            Path(f'{md_path}/{foldername}').mkdir(parents=True, exist_ok=True)   

            identifiers = {}
            for item in value["identifiers"]:
                # split identifiers in dict
                [key, value] = item.split(':',1)
                identifiers[key] = value          

            # marcxml data:        
            if marc == 'True':     

                # get mms_id
                mmsid = identifiers['mmsid']

                # get SRU response
                query = marc_url+mmsid
                response = requests.get(query)
                if response.status_code != 200:
                    raise Exception(f"SRU request failed with status code {response.status_code}")

                # Save the response content as xml to a new directory
                marcxmlfile = f"{md_path}/{foldername}/{mmsid}.xml"

                with open(marcxmlfile, 'wb') as file:
                    file.write(response.content)
                    print(f"#{counter}-{mmsid} Marc XML downloaded.")


            # datacite metadata        
            if (datacite == "True"):       

                # get zenodo id and start OAI-PMH request
                zenodo_id = identifiers['zenodo']
                sickle = Sickle(zenodo_url)            
                datacite_response = sickle.GetRecord(identifier=f"oai:zenodo.org:{zenodo_id}", metadataPrefix='oai_datacite')
                datacitefile = f'{md_path}/{foldername}/{zenodo_id}_datacite.xml'

                with open(datacitefile, 'w', encoding="utf-8") as file:
                    file.write(datacite_response.raw)
                    print(f'#{counter} - {zenodo_id}: Datacite Metadata downloaded. ')

                # wait 1 second every 10 records so as not to overshoot zenodo rate limiting. 
                if counter%10 == 0: time.sleep(1)

            # dublincore metadata        
            if (dublincore == "True"):  

                # get zenodo id and start OAI-PMH request
                zenodo_id = identifiers['zenodo']
                sickle = Sickle(zenodo_url)            
                dc_response = sickle.GetRecord(identifier=f"oai:zenodo.org:{zenodo_id}", metadataPrefix='oai_dc')
                dc_file = f'{md_path}/{foldername}/{zenodo_id}_dc.xml'

                with open(dc_file, 'w', encoding="utf-8") as file:
                    file.write(dc_response.raw)
                    print(f'#{counter} - {zenodo_id}: DC Metadata downloaded. ')

                # wait 1 second every 10 records so as not to overshoot zenodo rate limiting. 
                if counter%10 == 0: time.sleep(1)        
                    
            # zenodo api metadata        
            if (apidata == "True"):  

                # get zenodo id and start http request
                zenodo_id = identifiers['zenodo']
                # get Zenodo-API response
                query = f'{zenodo_api}/{zenodo_id}'
                response = requests.get(query)
                if response.status_code != 200:
                    raise Exception(f"API request failed with status code {response.status_code}")

                # Save the response content as json to a new directory
                zenodo_json = f"{md_path}/{foldername}/{zenodo_id}.json"

                with open(zenodo_json, 'wb') as file:
                    file.write(response.content)
                    print(f"#{counter} - {zenodo_id}: JSON Record downloaded.")

                # wait 1 second every 10 records so as not to overshoot zenodo rate limiting. 
                if counter%10 == 0: time.sleep(1)  
                    
            # e-codices api metadata        
            if (tei == "True"):  

                # get ecodices_url and start http request
                tei_id = identifiers['e-codices']
                # get E-Codices response
                query = f'{ecodices_url}/{tei_id}'               

                response = requests.get(query)    
                if response.status_code != 200:
                    query = f'{ecodices_url}/{tei_id}_Kamber'
                    response = requests.get(query)
                    
                    if response.status_code != 200:
                        query = f'{ecodices_url}/{tei_id}_Bretscher'
                        response = requests.get(query)
                        
                        if response.status_code != 200:
                            print(query)
                            raise Exception(f"API request failed with status code {response.status_code}")
                    
                print(query)
                # Save the response content as json to a new directory
                tei_published = f"{md_path}/{foldername}/{tei_id}.xml"

                with open(tei_published, 'wb') as file:
                    file.write(response.content)
                    print(f"#{counter} - {tei_id}: XML Description downloaded.")


    
print("Finished at ",datetime.today().strftime('%Y-%m-%d %H:%M:%S'))