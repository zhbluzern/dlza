import json
from pathlib import Path
import pandas as pd
import os
import zipfile
import shutil
import stat

class dlzaHandler:
    def __init__(self,logger,collection,foldername,baseDir=""):
        self.logger = logger
        self.collection = collection
        self.foldername = foldername
        self.baseDir = baseDir
        self.dlzaDirs = self.createFolders()

    # 📂 create subfolders, if they do not exist already:
    def createFolders(self):
        listOfSubDirectories = ["data","metadata","ingest"]
        dictOfDir = {"collectionRoot": f'{self.baseDir}{self.collection}', "recordDir":f'{self.baseDir}{self.collection}/{self.foldername}' }
        for subDir in listOfSubDirectories:
            dataDir = f'{self.baseDir}{self.collection}/{self.foldername}/{subDir}/'
            Path(dataDir).mkdir(parents=True, exist_ok=True)
            dictOfDir.update({subDir:dataDir})
            self.logger.log(f"📂 Directory {dataDir} created")
        return dictOfDir

    def writeInfoSetJson(self, infoSet):
        # Write the infoSet to a JSON file
        info_json = json.dumps(infoSet, indent=4, ensure_ascii=False)
        #infofile = f"{self.baseDir}{self.collection}/{self.foldername}/ingest/info.json"
        infofile = f"{self.dlzaDirs["ingest"]}info.json"

        with open(infofile, "w", encoding="utf-8") as outfile:
            outfile.write(info_json)
            self.logger.log(f"💾 info.json saved as {infofile}")

    # Writing completeSet as JSON
    def writeCompleteSet(self, completeSet, fulljsonfile="completeSet.json"):
        fulldump = json.dumps(completeSet, indent=4, ensure_ascii=False)
        self.logger.log(f"💾 write completeset to {fulljsonfile}")
        with open(fulljsonfile, "w", encoding="utf-8") as outfile:
            outfile.write(fulldump)
            self.logger.log(f"===============================")
            self.logger.log(f"💾 All Inventory JSON written to {fulljsonfile}")
        return True

    # 📦 ZIP-Archiv erstellen
    def make_writable_recursive(self, path):
        for root, dirs, files in os.walk(path):
            # Make all subdirectories writable
            for d in dirs:
                os.chmod(os.path.join(root, d), stat.S_IWRITE)
            # Make all files writable
            for f in files:
                os.chmod(os.path.join(root, f), stat.S_IWRITE)
        # Also make the root directory writable
        os.chmod(path, stat.S_IWRITE)

    def zip_directory(self, source_dir, zip_path, rmSourceDir=False):
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    # Preserve relative path inside the zip
                    rel_path = os.path.relpath(full_path, start=source_dir)
                    zipf.write(full_path, arcname=rel_path)
        self.logger.log(f"📦 {source_dir} packed as {zip_path}")

        if rmSourceDir==True:
            self.make_writable_recursive(source_dir)
            shutil.rmtree(source_dir)
            self.logger.log(f"🗑️ {source_dir} removed")

