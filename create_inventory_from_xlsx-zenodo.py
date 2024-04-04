import json
import pandas as pd
import config
from datetime import datetime

# needed variables: files, paths, input

input_file = config.input_file
collection = config.collection_id
info_dir = f'{collection}/{config.info_path}/'
urn = config.ingest_workflow
org_id = config.organisation_id
coll_id = config.collection_id
fulljsonfile = f'{config.inventory_file}'
fullexcelfile = f'{config.inventory_xlsx}'

completeSet = []

today = datetime.today().strftime('%Y-%m-%d')
now = datetime.now().isoformat()
doc_counter = 0

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
        "additional": row["filepath"]
    }
    
    # identifiers
        
    doi = row['doi']
    zenodo_id = str(row['zenodo_id'])
    
    # folder name and signature:
    foldername = doi.replace('.','_').replace('/','_')
    signature = f'{org_id}:{coll_id}_{foldername}'
        
    #complete info.json    
    infoSet["identifiers"] = ['doi:'+doi, 'zenodo:'+zenodo_id]
    infoSet["signature"] = signature
    infoSet["references"] = [row["reference"], foldername]

    #print(infoSet)    
    completeSet.append(infoSet)
    
    # Write the infoSet to a JSON file
    info_json = json.dumps(infoSet, indent=4, ensure_ascii=False)
    infofile = f"{info_dir}{foldername}.json"

    with open(infofile, "w", encoding="utf-8") as outfile:
        outfile.write(info_json)
        print(f"info.json saved as {infofile}")
        

# Writing completeSet as json file
fulldump = json.dumps(completeSet, indent=4, ensure_ascii=False)

with open(fulljsonfile, "w", encoding="utf-8") as outfile:
    outfile.write(fulldump)
    print(f"---\nAll JSON written to {fulljsonfile}")
    
# Writing completeSet as Excel file

df_json = pd.read_json(fulljsonfile)
df_json.to_excel(fullexcelfile)
print(f"All data saved to Excel file as {fullexcelfile}")
print(f"Total records: {doc_counter}\nFinished at {now}")