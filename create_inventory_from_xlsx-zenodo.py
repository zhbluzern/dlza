import json
import pandas as pd
import config
from datetime import datetime
from pathlib import Path

# needed variables: files, paths, input

input_file = config.input_file
collection = config.collection_id
urn = config.ingest_workflow
org_id = config.organisation_id
coll_id = config.collection_id
fulljsonfile = f'{collection}/{collection}_inventory.json'
fullexcelfile = f'{collection}/{collection}_inventory.xlsx'

completeSet = []

today = datetime.today().strftime('%Y-%m-%d')
now = datetime.now().isoformat()
doc_counter = 0

# create folder for current collection, if it does not exist already:
Path(f'{collection}').mkdir(parents=True, exist_ok=True)

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(input_file)

for _, row in df.iterrows():

    doc_counter += 1
    infoSet = { 
        # infoset created after https://github.com/je4/gocfl/blob/main/gocfl-info-1.0.json 

        "signature": "",
        "organisation_id": org_id,
        "organisation": config.organisation,
        "organisation_address": config.organisation_address,
        "collection_id": coll_id,
        "collection": config.collection,
        "sets": config.sets,
        "identifiers": [],
        "title": row['title'],
        "alternative_titles": [],
        "description": "",
        "keywords": config.keywords,
        "user": config.user_name,
        "address": config.user_address,
        "created": row["created"],
        "last_changed": now,
        "deprecates": "",
        "references": "",
        "ingest_workflow": urn,
        "additional": []
    }
    
    # identifiers
        
    doi = row['doi']
    zenodo_id = str(row['zenodo_id'])
    concept_id = str(row['concept_id'])
    filepath = row["filepath"]
    license = row["license"]

    
    # folder name and signature:
    foldername = doi.replace('.','_').replace('/','_')
    signature = f'{org_id}:{coll_id}_{foldername}'

    # create subfolders, if they do not exist already:
    Path(f'{collection}/{foldername}/data').mkdir(parents=True, exist_ok=True)
    Path(f'{collection}/{foldername}/metadata').mkdir(parents=True, exist_ok=True)
    Path(f'{collection}/{foldername}/ingest').mkdir(parents=True, exist_ok=True)
    
        
    #complete info.json    
    infoSet["identifiers"] = ['doi:'+doi, 'zenodo:'+zenodo_id, 'concept:'+concept_id]
    infoSet["signature"] = signature
    infoSet["references"] = [row["reference"], 'sip:'+foldername]
    infoSet["additional"] = [filepath, license]

    #print(infoSet)    
    completeSet.append(infoSet)
    
    # Write the infoSet to a JSON file
    info_json = json.dumps(infoSet, indent=4, ensure_ascii=False)
    infofile = f"{collection}/{foldername}/ingest/info.json"

    with open(infofile, "w", encoding="utf-8") as outfile:
        outfile.write(info_json)
        print(f"info.json saved as {infofile}")
        

# Writing completeSet as json file
fulldump = json.dumps(completeSet, indent=4, ensure_ascii=False)

with open(fulljsonfile, "w", encoding="utf-8") as outfile:
    outfile.write(fulldump)
    print(f"---\nAll Inventory JSON written to {fulljsonfile}")
    
# Writing completeSet as Excel file

df_json = pd.read_json(fulljsonfile)
df_json.to_excel(fullexcelfile)
print(f"All data saved to Excel file as {fullexcelfile}")
print(f"Total records: {doc_counter}\nFinished at {now}")