import requests
import pandas as pd
import datetime 
import config

community = config.collection_id
output = config.input_file
zenodoRestUrl = config.baseurl_zenodo_api
headers = {}
headers["Content-Type"] = "application/json"
size = '100'
params = { "communities":  community, "size": size}


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
        resultDet["license"] = record["metadata"]["license"]["id"]    

        print(f"#{localRecordCounter}: {record['doi']}")

        localRecordCounter += 1
        resultSet.append(resultDet)
    remotePaginator += 1
    print(f"go to next {size} records page {remotePaginator}")

print(f"Number of Records writing to file: {localRecordCounter-1}")

#Schreibe Metadaten (resultSet) in ein XLS-File zur Weiterbearbeitung
df = pd.DataFrame(resultSet) 
#print(df.head())
df.to_excel(output) 
print("Finished at:", datetime.datetime.now())