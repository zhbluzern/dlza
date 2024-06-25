import config
from datetime import datetime
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
ona_conf = config.ona_conf
gocfl = config.gocfl

# input file
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
        #print("           Storage root: ",storage_root)
        dir_metadata = f'{root}/{metadata}/{foldername}/'
        #print("           Metadata folder: ",dir_metadata)
        f_infojson = f'{root}/{info}/{foldername}.json'        
        #print("           Info.json: ",f_infojson)
        dir_sip = f'{root}/{objects}/{foldername}/'
        #print("           SIP folder: ",dir_sip)
        
        # create string  
        create_string = f'{gocfl} create {storage_root} {dir_sip} metadata:{dir_metadata} -i {signature} --ext-NNNN-metafile-source file://{f_infojson} --config {gocfl_conf}'
        print(f'\n###############\n{create_string}\n###############\n')
        
        # display string
        display_string = f'{gocfl} display {storage_root}'

        # ona string TODO example:
        #ona_string = f'ona ingest -w -p D:\Ingest\zhb_lory_zhb_10_5281_zenodo_10175.zip -c D:\Ingest\config\ona-config.yml'
        ona_string = f'ona ingest -w -p {storage_root} -c {ona_conf}'
        
        # write strings to file
        create_file = f'{coll}/{files}/{foldername}_create.bat'
        display_file = f'{coll}/{files}/{foldername}_display.bat'
        ona_file = f'{coll}/{files}/{foldername}_ona.bat'
        with open(create_file, 'w', encoding="utf-8", errors='replace') as file:
            file.write(create_string)

        with open(display_file, 'w', encoding="utf-8", errors='replace') as file:
            file.write(display_string)

        with open(ona_file, 'w', encoding="utf-8", errors='replace') as file:
            file.write(ona_string)


               
print("Finished at ",datetime.today().strftime('%Y-%m-%d %H:%M:%S'))                