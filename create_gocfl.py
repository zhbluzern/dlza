import config
from datetime import datetime
import json

#prepare archive structure
root = config.dlza_root
collection = config.collection_id
org = config.organisation_id

gocfl_conf = config.gocfl_conf
ona_conf = config.ona_conf
gocfl = config.gocfl

# input file
file_name = f'{collection}/{collection}_inventory.json'

# read line from file
with open(file_name, encoding="utf-8", errors='replace') as data_file:    
    data = json.load(data_file)
    for value in data:
        
        signature = value["signature"]
        sip = value["references"][-1][4:]
        #print("foldername:",foldername)

        
        # create filepaths for metadata, info.json, objects:
        storage_root = f'{root}/{collection}_{sip}.zip' 
        print("           Storage root: ",storage_root)
        dir_metadata = f'{root}/{collection}/{sip}/metadata'
        print("           Metadata folder: ",dir_metadata)
        f_infojson = f'{root}/{collection}/{sip}/ingest/info.json'        
        print("           Info.json: ",f_infojson)
        dir_sip = f'{root}/{collection}/{sip}/data'
        print("           SIP folder: ",dir_sip)
        
        # create string  
        create_string = f'{gocfl} create {storage_root} {dir_sip} metadata:{dir_metadata} -i {signature} --ext-NNNN-metafile-source file://{f_infojson} --config {gocfl_conf}'
        create_string+='\nRead-Host -Prompt "Press Enter to exit"'
        #print(create_string)
        
        # display string
        display_string = f'{gocfl} display {storage_root}'

        # ona ingest / stored
        ona_ingest = f'ona ingest -w -p {storage_root} -c {ona_conf}'
        ona_ingest+='\nRead-Host -Prompt "Press Enter to exit"'
        ona_stored = f'ona stored -n {storage_root} -c {ona_conf}'
        ona_stored+='\nRead-Host -Prompt "Press Enter to exit"'
        
        # write strings to file
        create_file = f'{collection}/{sip}/ingest/{sip}_create.ps1'
        display_file = f'{collection}/{sip}/ingest/{sip}_display.ps1'
        ona_ingest_file = f'{collection}/{sip}/ingest/{sip}_ona_ingest.ps1'
        ona_stored_file = f'{collection}/{sip}/ingest/{sip}_ona_stored.ps1'

        with open(create_file, 'w', encoding="utf-8", errors='replace') as file:
            file.write(create_string)

        with open(display_file, 'w', encoding="utf-8", errors='replace') as file:
            file.write(display_string)

        with open(ona_ingest_file, 'w', encoding="utf-8", errors='replace') as file:
            file.write(ona_ingest)

        with open(ona_stored_file, 'w', encoding="utf-8", errors='replace') as file:
            file.write(ona_stored)

               
print("Finished at ",datetime.today().strftime('%Y-%m-%d %H:%M:%S'))                