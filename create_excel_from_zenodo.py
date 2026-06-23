import requests
import pandas as pd
import datetime 
import config
import time

# This script harvests records from a Zenodo community and writes the metadata to an Excel file.
# Make sure to have the required libraries installed:
# pip install requests pandas openpyxl

# Set the community ID and harvest date
community = config.collection_id
# enter the date from which you want to harvest records, e.g. "2024-07-19" for all records from 19th July 2024 onwards. Default (all records) is: "1970-01-01"
harvest_from_date = "1970-01-01" #default
#harvest_from_date = "2025-07-08" # last import date


output = config.input_file
zenodoRestUrl = config.baseurl_zenodo_api
headers = {}
headers["Content-Type"] = "application/json"
size = '25' # for higher page size you need an API token
params = { "communities":  community, "size": size, "q": f"created:[{harvest_from_date} TO *]" }


def getRecords(max_retries=5):
    for attempt in range(max_retries):
        r = requests.get(f"{zenodoRestUrl}", params=params, headers=headers)

        # ✅ Erfolg
        if r.status_code == 200:
            return r.json()

        # ✅ 204 = kein Inhalt
        if r.status_code == 204:
            return None

        # ✅ 429 = warten + retry
        if r.status_code == 429:
            #wait = int(r.headers.get("Retry-After", 2))
            wait = int(r.headers.get("Retry-After", 2)) * (2 ** attempt)
            time.sleep(wait)
            continue

        # ✅ andere Fehler → abbrechen
        r.raise_for_status()

    raise Exception("Max retries überschritten")


result = getRecords()
numOfRec = (result["hits"]["total"])
print(f"Number of Records in Community {community}: {numOfRec}")

localRecordCounter = 1
remotePaginator = 1
resultSet = []
while localRecordCounter < int(numOfRec):
    params["page"] = remotePaginator
    result = getRecords()
    for record in result["hits"]["hits"]:
        resultDet = {}
        resultDet["created"] = record["updated"]
        resultDet["doi"] = record["doi"]
        resultDet["zenodo_id"] = record["recid"]
        resultDet["concept_id"] = record["conceptrecid"]
        resultDet["reference"] = record["doi_url"]
        resultDet["title"]= record["metadata"]["title"]
        resultDet["filepath"]= record["links"]["files"]
        #resultDet["license"] = record["metadata"]["license"]["id"]        
        resultDet["license"] = record["metadata"].get("license", {}).get("id", "unlicensed")

        
        # Check if already in DLZA: search for identifier starting with 'zhb' in the related_identifiers
               
        dlza_identifier = None
        
        related = record["metadata"].get("related_identifiers", [])
        if isinstance(related, list):
            for entry in related:
                if (entry.get('relation', '').lower() == 'isidenticalto' and entry.get('identifier', '').lower().startswith('zhb')):
                    dlza_identifier = entry['identifier']
                    break

        print(dlza_identifier)
        resultDet["dlza_identifier"] = dlza_identifier if dlza_identifier else "none"

        print(f"#{localRecordCounter}: {record['doi']}")
        time.sleep(0.2)

        localRecordCounter += 1
        resultSet.append(resultDet)
    remotePaginator += 1
    print(f"go to next {size} records page {remotePaginator}")

print(f"Number of Records writing to file: {localRecordCounter-1}")

#Schreibe Metadaten (resultSet) in ein XLSX-File zur Weiterbearbeitung
df = pd.DataFrame(resultSet) 
#print(df.head())
df.to_excel(output) 
print("Finished at:", datetime.datetime.now())