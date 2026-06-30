import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os
from sickle import Sickle
from requests.exceptions import HTTPError
import config
import time

GLOBAL_DELAY = 0.3

# get access token for Zenodo API
load_dotenv()
ACCESS_TOKEN = os.getenv('access_token')

# which metadata is available:
marc = config.marcxml
mods = config.mods
mets = config.mets
datacite = config.datacite
dublincore = config.dc
zenodomarc = config.zenodomarc
zenodoapi = config.zenodoapi
tei = config.tei

marc_url = config.baseurl_marc
mods_url = config.baseurl_mods
mets_url = config.baseurl_mets
zenodo_oai_url = config.baseurl_zenodo_oai
zenodo_api_url = config.baseurl_zenodo_api
tei_url = config.baseurl_tei

# general config:

urn = config.ingest_workflow
collection = config.collection_id
org_id = config.organisation_id

input_file = f'{collection}/{collection}_inventory.json'
counter = 0
debug = 9999 # debug mode. How many records are harvested. Enter 9999 for production mode.

# 🔥 hier einstellen, bei welcher Excelzeile du wieder anfangen willst, wenn es abgebrochen ist. Default: 0
start_at = 0

#zentrale funktion für alle OAI records

def fetch_oai_record(sickle, zenodo_id, prefix, label):
    def request():
        return sickle.GetRecord(
            identifier=f"oai:zenodo.org:{zenodo_id}",
            metadataPrefix=prefix
        )

    for attempt in range(5):
        try:
            result = request()
            return result

        except Exception as e:
            wait = 2 ** attempt
            print(f"⚠️ {label} Fehler ({zenodo_id}) → retry in {wait}s")
            time.sleep(wait)

    print(f"❌ {label} komplett fehlgeschlagen: {zenodo_id}, Zeile {counter}")
    return None

# funktion für Zenodo API

def fetch_json(url, params=None):
    for attempt in range(5):
        try:
            r = requests.get(url, params=params, timeout=10)

            if r.status_code == 200:
                return r

            if r.status_code == 429:
                wait = int(r.headers.get("Retry-After", 2))
                time.sleep(wait)
                continue

            r.raise_for_status()

        except requests.exceptions.ConnectionError:
            wait = 2 ** attempt
            time.sleep(wait)

    return None




with open(input_file, encoding="utf-8", errors="replace") as data_file:    
    data = json.load(data_file)
    for value in data:
        
        counter+= 1
        #time.sleep(GLOBAL_DELAY)
        
        
        if counter < start_at:
            continue   # 🔥 überspringt alles bis zu dieser Zeile im Excel
        
        
        if counter<= debug: 
            
            time.sleep(GLOBAL_DELAY)

            # create new directory for each signature (ignore, if it already exists)            
            foldername = value["references"][-1][4:]

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
                marcxmlfile = f"{collection}/{foldername}/metadata/{mmsid}.xml"

                with open(marcxmlfile, 'wb') as file:
                    file.write(response.content)
                    print(f"#{counter}-{mmsid} Marc XML downloaded.")

            # mods data:        
            if mods == 'True':     

                # get mms_id
                mmsid = identifiers['mmsid']

                # get SRU response
                query = mods_url+mmsid
                response = requests.get(query)
                if response.status_code != 200:
                    raise Exception(f"SRU request failed with status code {response.status_code}")

                # Save the response content as xml to a new directory
                modsfile = f"{collection}/{foldername}/metadata/{mmsid}_mods.xml"

                with open(modsfile, 'wb') as file:
                    file.write(response.content)
                    print(f"#{counter}-{mmsid} MODS XML downloaded.")        

            # mets data:
            if mets == 'True':

                # get external id:
                mets_id = identifiers['e-manuscripta']
                sickle = Sickle(mets_url) 
                mets_response = sickle.GetRecord(identifier=mets_id, metadataPrefix='mets')
                mets_file = f'{collection}/{foldername}/metadata/{mets_id}_mets.xml'
                with open(mets_file, 'w', encoding="utf-8") as file:
                    file.write(mets_response.raw)
                    print(f'#{counter}-{mets_id}: METS file downloaded. ')

            # datacite metadata
            if datacite == "True":
                zenodo_id = identifiers['zenodo']
                sickle = Sickle(zenodo_oai_url)
            
                time.sleep(0.5)  # 🔥 wichtig!
            
                res = fetch_oai_record(sickle, zenodo_id, 'oai_datacite', 'Datacite')
            
                if res:
                    file = f'{collection}/{foldername}/metadata/{zenodo_id}_datacite.xml'
                    with open(file, 'w', encoding="utf-8") as f:
                        f.write(res.raw)
                        print(f'#{counter} - {zenodo_id}: Datacite Metadata downloaded. ')
                        
            #dublincore metadata
            if dublincore == "True":
                zenodo_id = identifiers['zenodo']
                sickle = Sickle(zenodo_oai_url)
            
                time.sleep(0.5)
            
                res = fetch_oai_record(sickle, zenodo_id, 'oai_dc', 'DublinCore')
            
                if res:
                    file = f'{collection}/{foldername}/metadata/{zenodo_id}_dc.xml'
                    with open(file, 'w', encoding="utf-8") as f:
                        f.write(res.raw)
                        print(f'#{counter} - {zenodo_id}: DC Metadata downloaded. ')


 
            #marcxml metadata Zenodo
            if zenodomarc == "True":
                zenodo_id = identifiers['zenodo']
                sickle = Sickle(zenodo_oai_url)
            
                time.sleep(0.5)
            
                res = fetch_oai_record(sickle, zenodo_id, 'marcxml', 'ZenodoMARC')
            
                if res:
                    file = f'{collection}/{foldername}/metadata/{zenodo_id}_marc.xml'
                    with open(file, 'w', encoding="utf-8") as f:
                        f.write(res.raw)
                        print(f'#{counter} - {zenodo_id}: Zenodo-MARC Metadata downloaded. ')
            
                         
                    
            # zenodo api metadata        
            if zenodoapi == "True":  

                retry_count = 0
                max_retries = 5
                # get zenodo id and start http request
                zenodo_id = identifiers['zenodo']
                # get Zenodo-API response
                query = f'{zenodo_api_url}/{zenodo_id}'
                time.sleep(1)
                
                response = fetch_json(query, {'access_token': ACCESS_TOKEN})

                #response = requests.get(query, params={'access_token': ACCESS_TOKEN})
                if response.status_code != 200:
                    raise Exception(f"API request failed with status code {response.status_code}")

                # Save the response content as json to a new directory
                zenodo_json = f"{collection}/{foldername}/metadata/{zenodo_id}.json"

                with open(zenodo_json, 'wb') as file:
                    file.write(response.content)
                    print(f"#{counter} - {zenodo_id}: JSON Record downloaded.")

                # wait 1 second every 10 records so as not to overshoot zenodo rate limiting. 
                if counter%10 == 0: time.sleep(1)  
                    
            # e-codices TEI metadata        
            if (tei == "True"):  

                # get ecodices_url and start http request
                tei_id = identifiers['e-codices']
                # get E-Codices response
                query = f'{tei_url}/{tei_id}'               

                response = requests.get(query)    
                if response.status_code != 200:
                    query = f'{tei_url}/{tei_id}_Kamber'
                    response = requests.get(query)
                    
                    if response.status_code != 200:
                        query = f'{tei_url}/{tei_id}_Bretscher'
                        response = requests.get(query)
                        
                        if response.status_code != 200:
                            print(query)
                            raise Exception(f"API request failed with status code {response.status_code}")
                    
                print(query)
                # Save the response content as json to a new directory
                tei_published = f"{collection}/{foldername}/metadata/{tei_id}.xml"

                with open(tei_published, 'wb') as file:
                    file.write(response.content)
                    print(f"#{counter} - {tei_id}: XML Description downloaded.")


    
print("Finished at ",datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
