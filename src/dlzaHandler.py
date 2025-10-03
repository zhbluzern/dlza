import json
from pathlib import Path
import pandas as pd

def createFolders(collection,foldername,baseDir=""):
    # create subfolders, if they do not exist already:
    dataDir = f'{baseDir}{collection}/{foldername}/data/'
    Path(dataDir).mkdir(parents=True, exist_ok=True)
    metadataDir = f'{baseDir}{collection}/{foldername}/metadata/'
    Path(metadataDir).mkdir(parents=True, exist_ok=True)
    ingestDir = f'{baseDir}{collection}/{foldername}/ingest/'
    Path(ingestDir).mkdir(parents=True, exist_ok=True)
    return {"data": dataDir, "metadata": metadataDir, "ingest": ingestDir}

def writeInfoSetJson(infoSet,collection,foldername,logger,baseDir=""):
    # Write the infoSet to a JSON file
    info_json = json.dumps(infoSet, indent=4, ensure_ascii=False)
    infofile = f"{baseDir}{collection}/{foldername}/ingest/info.json"

    with open(infofile, "w", encoding="utf-8") as outfile:
        outfile.write(info_json)
        logger.log(f"info.json saved as {infofile}")

# Writing completeSet as JSON
def writeCompleteSet(completeSet,logger,fulljsonfile="completeSet.json"):
    fulldump = json.dumps(completeSet, indent=4, ensure_ascii=False)
    logger.log(f"write completeset to {fulljsonfile}")
    with open(fulljsonfile, "w", encoding="utf-8") as outfile:
        outfile.write(fulldump)
        logger.log(f"---\nAll Inventory JSON written to {fulljsonfile}")
    return True

# # 📦 ZIP-Archiv erstellen
# zip_path = os.path.join(local_dir, zip_filename)
# with ZipFile(zip_path, 'w') as zipf:
#     for file in remote_files:
#         local_file = os.path.join(local_dir, os.path.basename(file))
#         zipf.write(local_file, arcname=os.path.basename(file))

# print(f'ZIP archive created: {zip_path}')