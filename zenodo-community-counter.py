import requests
import pandas as pd
import datetime 
import openpyxl

# Script to check if all necessary LORY communities are there before starting DLZA
# enter community name (lory_unilu, lory_hslu, lory_phlu)
# output: Excel file with basic zenodo id, title and all linked communities.
# quick sort trick in excel: sort communities (first lory, then lory_school, then lory_school_department, etc.). There should minimum be 3 communities (except phlu: 2)
# switch values within excel columns by drag & drop, to check that all necessary communities are there: 
# 1. markieren Sie die Werte, die Sie verschieben möchten. 
# 2. Bewegen Sie dann den Mauszeiger an den Rand der Spalte, bis er sich in einen vierseitigen Pfeil verwandelt. 
# 3. Halten Sie die Umschalttaste und die linke Maustaste gedrückt und ziehen Sie die Spalte an die neue Position. Eine grüne Linie zeigt die neue Position an. Lassen Sie die Maustaste und die Umschalttaste los, um die Spalte zu verschieben.

# TODO: script stops working for big communities (Gateway timeout). Last checked: 01.07.2025 / update get request to only check new records (published or updated after last check)

community = 'lory_hslu'
# community = 'lory_unilu'
# community = 'lory_phlu'

output = f'{community}_communities.xlsx'
zenodoRestUrl = "https://zenodo.org/api/records"
headers = {}
headers["Content-Type"] = "application/json"
size = '100'


params = { "communities":  community, "size": size}


def getRecords():
    r = requests.get(f"{zenodoRestUrl}", params=params, headers=headers)
    try:
        return r.json()
    except requests.exceptions.JSONDecodeError:
        print(f"[ERROR] Failed to decode JSON on page: {params.get('page', 1)}")
        print(f"[DEBUG] Status Code: {r.status_code}")
        print(f"[DEBUG] Content: {r.text[:200]}")  # Peek at the first 200 chars
        return None

result = getRecords()
numOfRec = (result["hits"]["total"])
print(f"Number of Records in Community {community}: {numOfRec}")

localRecordCounter = 1
remotePaginator = 1
resultSet = []
while localRecordCounter < int(numOfRec):
    params["page"] = remotePaginator
    result = getRecords()
    if not result or "hits" not in result:
        print("Terminating at this page due to invalid or empty response.")
        remotePaginator += 1
        print(remotePaginator)
        break
        
    for record in result["hits"]["hits"]:
        resultDet = {}
        resultDet["doi"] = record["doi"]
        resultDet["url"] = record["doi_url"]
        resultDet["title"]=(record["metadata"]["title"])
        resultDet["owner"]=(record["owners"])
        print(f"#{localRecordCounter}: ")
        communitycounter = 1
        for communities in record["metadata"]["communities"]:
            print(communities["id"])
            resultDet[f"community{communitycounter}"]=(communities["id"])
            communitycounter+= 1

        localRecordCounter += 1
        resultSet.append(resultDet)
    #Schreibe Metadaten (resultSet) in ein XLS-File zur Weiterbearbeitung
    df = pd.DataFrame(resultSet) 
    #print(df.head())
    df.to_excel(output)
    remotePaginator += 1
    print(f"go to next {size} records page {remotePaginator}")

print(f"Number of Records writing to file: {localRecordCounter}")

#Schreibe Metadaten (resultSet) in ein XLS-File zur Weiterbearbeitung
#df = pd.DataFrame(resultSet) 
#print(df.head())
#df.to_excel(output) 
print("Finished at:", datetime.datetime.now())