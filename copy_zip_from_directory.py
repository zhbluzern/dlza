import os
import config
import json
from datetime import datetime
import zipfile
import shutil
from pathlib import Path

localdrive = config.user_root
org_id = config.organisation_id
collection = config.collection_id

file_name = f'{collection}/{collection}_inventory.json'

counter = 0
debug = 0 # Test mode, for prod: set to higher number than total files in collection

with open(file_name, encoding="utf-8", errors='replace') as data_file:    
    data = json.load(data_file)
    for value in data:

        counter += 1

        #get sip folder. The full path is needed here for copying the files.
        sip_folder = value["identifiers"][-1][4:]
        data_path = f'{localdrive}/{collection}/{sip_folder}/data/'
        # get path to G drive:
        g_path = value["additional"][0]

        filenames = []
        # Iterate directory, check if current file_path is a file
        try:
            for file_path in os.listdir(g_path):
                #print("Origin files:", file_path)
                if os.path.isfile(os.path.join(g_path, file_path)):
                    filenames.append(file_path)
                else:
                    print("---------------- not a file!-----------------------")
        except FileNotFoundError:
            print(f"The directory {g_path} does not exist")
        except PermissionError:
            print(f"Permission denied to access the directory {g_path}")
        except OSError as e:
            print(f"An OS error occurred: {e}")
        
        if counter< debug:            


            filenames = []
            # Iterate directory, check if current file_path is a file
            try:
                for file_path in os.listdir(g_path):
                    print("Origin files:", file_path)
                    if os.path.isfile(os.path.join(g_path, file_path)):
                        filenames.append(file_path)
                    else:
                        print("---------------- not a file!-----------------------")
            except FileNotFoundError:
                print(f"The directory {g_path} does not exist")
            except PermissionError:
                print(f"Permission denied to access the directory {g_path}")
            except OSError as e:
                print(f"An OS error occurred: {e}")

            for file in filenames:   
                sip_file = Path(data_path+'/'+file)
                if sip_file.exists():
                    # path exists
                    print("*** Path exists, file already copied")
                else:
                    # copy file:
                    print("Copying file:", file)
                    print("Time started copying:",datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                    shutil.copy(g_path+'/'+file, data_path+'/'+file) 

                    print("File copied successfully.")
        else:
            print("**************\nYou are in test mode, no files are copied!\n*******************")
     

            
print("Finished at ",datetime.today().strftime('%Y-%m-%d %H:%M:%S'))