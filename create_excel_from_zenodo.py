import requests
import pandas as pd
import datetime 
import config

# This script harvests records from a Zenodo community and writes the metadata to an Excel file.
# Make sure to have the required libraries installed:
# pip install requests pandas openpyxl

# Set the community ID and harvest date
community = config.collection_id
# enter the date from which you want to harvest records, e.g. "2024-07-19" for all records from 19th July 2024 onwards. Default (all records) is: "1970-01-01"
harvest_from_date = "1970-01-01"

output = config.input_file
zenodoRestUrl = config.baseurl_zenodo_api
headers = {}
headers["Content-Type"] = "application/json"
size = '100'
params = { "communities":  community, "size": size, "q": f"created:[{harvest_from_date} TO *]" }


def getRecords():
    r = requests.get(f"{zenodoRestUrl}", params=params, headers=headers)
    r.raise_for_status()
    if r.status_code != 204:
        return r.json()

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