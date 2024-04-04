import config
import os
from zipfile import ZipFile
import shutil
from datetime import datetime
from pathlib import Path
import json

#prepare archive structure
root = config.dlza_root
coll = config.collection_id
org = config.organisation_id
files = config.gocfl_path
metadata =  f'{coll}/{config.metadata_path}'
info = f'{coll}/{config.info_path}'
objects = f'{coll}/{config.object_path}'
gocfl_conf = config.gocfl_conf
gocfl = config.gocfl

# filenames
f_create = f'{coll}/{files}/create_'
f_info = f'{config.inventory_file}'

# read line from file
with open(f_info, encoding="utf-8", errors='replace') as data_file:    
    data = json.load(data_file)
    for value in data:
        
        signature = value["signature"]
        foldername = value["references"][-1]
        print("foldername:",foldername)
        
        # create filepaths for metadata, info.json, objects:
        storage_root = f'{root}/{org}_{coll}_{foldername}.zip' 
        print("           Storage root: ",storage_root)
        dir_metadata = f'{root}/{metadata}/{foldername}/'
        print("           Metadata folder: ",dir_metadata)
        f_infojson = f'{root}/{info}/{foldername}.json'        
        print("           Info.json: ",f_infojson)
        dir_sip = f'{root}/{objects}/{foldername}/'
        print("           SIP folder: ",dir_sip)
        
        # create string  
        create_string = f'{gocfl} create {storage_root} {dir_sip} metadata:{dir_metadata} -i {signature} --ext-NNNN-metafile-source file://{f_infojson} --config {gocfl_conf}'
        print(f'\n###############\n{create_string}\n###############\n')
        
        # display string
        display_string = f'{gocfl} display {storage_root}'
        report_name = f'{org}_{coll}_{foldername}.pdf'
        
        # write strings to file
        create_file = f'{f_create}_{foldername}.txt'
        with open(create_file, 'w') as file:
            file.write(create_string)
            file.write('\n\n')
            file.write(display_string)
            file.write(f'\n\nSave report as: {report_name}')
               
print("Finished at ",datetime.today().strftime('%Y-%m-%d %H:%M:%S'))                