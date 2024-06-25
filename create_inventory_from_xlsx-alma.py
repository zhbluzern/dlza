import json
import pandas as pd
import config
from pathlib import Path
from datetime import datetime

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
        "title": "",
        "alternative_titles": [],
        "description": "",
        "keywords": config.keywords,
        "user": config.user_name,
        "address": config.user_address,
        "created": now,
        "last_changed": now,
        "deprecates": "",
        "references": [],
        "ingest_workflow": urn,
        "additional": []
    }
    
    # identifiers
        
    doi = row['DOI']
    mms_id = str(row['MMS ID'])
    callnumber = row['Call number']
    recnumber = str(row['Record number'])
    title = row['Title']
    sip_path = row['Dateipfad']
    external_id = str(row['externe ID'])
    
    # folder name and signature:
    foldername = doi.replace('.','_').replace('/','_')
    signature = f'{org_id}:{coll_id}_{foldername}'

    # create subfolders, if they do not exist already:
    Path(f'{collection}/{foldername}/data').mkdir(parents=True, exist_ok=True)
    Path(f'{collection}/{foldername}/metadata').mkdir(parents=True, exist_ok=True)
    Path(f'{collection}/{foldername}/ingest').mkdir(parents=True, exist_ok=True)
    
    # references
    doiurl = config.baseurl_doi+doi
    almaurl = config.baseurl_alma+mms_id
    license = row['License']
    
    #complete info.json
    
    infoSet["identifiers"] = ['doi:'+doi, 'mmsid:'+mms_id, org_id+':'+callnumber,'rec:'+recnumber, urn+':'+external_id]
    infoSet["references"] = [doiurl, almaurl, 'sip:'+foldername]
    infoSet["signature"] = signature
    infoSet["title"] = title
    infoSet["additional"] = [sip_path.replace('\\','/'), license]

    #print(infoSet)
    
    completeSet.append(infoSet)
    
    # Write the infoSet to a JSON file
    info_json = json.dumps(infoSet, indent=4, ensure_ascii=False)
    infofile = f"{collection}/{foldername}/metadata/info.json"

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


