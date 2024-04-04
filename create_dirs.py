import os
from datetime import datetime
import config
from pathlib import Path


mainfolder = config.collection_id

infofolder = config.info_path
metadatafolder = config.metadata_path
objectsfolder = config.object_path
gocflfolder = config.gocfl_path

# create folder for current collection, if it does not exist already:
Path(f'{mainfolder}').mkdir(parents=True, exist_ok=True)

# create subfolders, if they do not exist already:
Path(f'{mainfolder}/{infofolder}').mkdir(parents=True, exist_ok=True)

Path(f'{mainfolder}/{metadatafolder}').mkdir(parents=True, exist_ok=True)

Path(f'{mainfolder}/{objectsfolder}').mkdir(parents=True, exist_ok=True)

Path(f'{mainfolder}/{gocflfolder}').mkdir(parents=True, exist_ok=True)

# list all directories in current working directory:
print(f"This directory now contains the following sub-directories:\n\n")
        
rootdir = f'./{mainfolder}'
for file in os.listdir(rootdir):
    d = os.path.join(rootdir, file)
    if os.path.isdir(d):
        print(d)
        
print("\n\nFinished at ",datetime.today().strftime('%Y-%m-%d %H:%M:%S'))