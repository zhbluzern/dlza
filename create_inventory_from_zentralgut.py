import pandas as pd
import config
import re
from datetime import datetime
from pathlib import Path
from lxml import etree
import src.goobiHandler as goobiHandler 
import src.dlzaHandler as DLZA 
import src.goobiSSH as goobiSSHConn 
import src.almaHandler as almaAPI
import src.logger as log

# needed variables: files, paths, input
input_file = config.input_file
collection = config.collection_id
urn = config.ingest_workflow
org_id = config.organisation_id
coll_id = config.collection_id
baseDir = config.boilerplate #could be also an external hdd like "G:/etc/etc/"
fulljsonfile = f'{baseDir}{collection}/{collection}_inventory.json'
fullexcelfile = f'{baseDir}{collection}/{collection}_inventory.xlsx'
completeSet = []
today = datetime.today().strftime('%Y-%m-%d')
now = datetime.now().isoformat()

# Initialize Logger
logger = log.SimpleLogger('logs/zentralgut_inventory.log')

# Initialize Goobi-Classes
goobi = goobiHandler.goobiHandler()
goobiSSH = goobiSSHConn.goobiSSHConn(logger)
s3Conn = goobiSSHConn.goobiS3Conn(logger)

# Initialize Alma-Class
alma = almaAPI.ExL_Bib()

# create folder for current collection, if it does not exist already:
Path(f'{baseDir}{collection}').mkdir(parents=True, exist_ok=True)

# Run through given ZentralGut-OAI-Set(s) and harvest all records
# : Create the zentralgut-collection
# : Create for each record a info.json file
# : Create for each record the directory-structure (\data, \ingest, \metadata)

    
for goobiSyntaxFilter in config.zentralgut_filter:
    #goobiFilter = {"filter": f"meta:UnsereGeschichteEntryID:{entryId}"}
    records = goobi.queryWorkflow(filterObject={"filter":goobiSyntaxFilter})
    #print(records)
    logger.log(f"🔎 Asked Goobi for the following list of {str(len(records['ids']))} records:")
    logger.log(records)

logger.log(f"⏳ Starting with creation of inventory for {collection} with {str(len(records['ids']))} records.")

for i, recordId in enumerate(records["ids"]):
    logger.log(f"📝 Processing record no. {str(i+1).zfill(4)} with ID: {recordId}")
    
    #Fetching Metadata for current Document
    processData = goobi.getProcess(recordId)
    metadata = goobi.getMetadata(recordId)
    zentralGutId = goobi.getMetadataDetail(metadata,metadataNames=["CatalogIDDigital"])
    ark = goobi.getMetadataDetail(metadata,metadataNames=["ARK"])
    title = goobi.getMetadataDetail(metadata,metadataNames=["TitleDocMain"])

    metsFile = goobi.getSourceFile(zentralGutId[0]["value"])
    if metsFile != None:
        license = metsFile.xpath(".//mods:accessCondition[@type='use and reproduction']/@xlink:href",namespaces=goobi.namespaces)
    else:
        license = [""]
    #print(license[0])

    # folder name and signature:
    foldername = ark[0]["value"].replace(':','').replace('/','_')
    signature = f'{org_id}:{coll_id}_{foldername}'
    
    # Create Subfolders for current Document
    dlza = DLZA.dlzaHandler(logger,collection,foldername,baseDir=config.boilerplate)

    #complete info.json    
    infoSet = dlza.loadInfoSet()
    infoSet["title"] = title[0]["value"]
    infoSet["identifiers"] = [ark[0]["value"], f'zentralgut_CatalogIDDigital:{zentralGutId[0]["value"]}', f'goobi_processId:{recordId}']
    infoSet["signature"] = signature
    infoSet["references"] = [f"https://n2t.net/{ark[0]["value"]}", goobi.getSourceFileUrl(zentralGutId[0]["value"]), 'sip:'+foldername] 
    infoSet["additional"] = [f"file:///opt/digiverso/viewer/media/{zentralGutId[0]["value"]}/", license[0]]


    # Download goobi.meta.xml and goobi.meta_anchor.xml Files
    remote_dir = f"/opt/digiverso/goobi/metadata/{recordId}/"
    remote_dirRuleSet = "/opt/digiverso/goobi/rulesets/"
    metaLs = goobiSSH.sftp.listdir(remote_dir)
    for metaFile in metaLs:
        if metaFile == "meta.xml" or metaFile == "meta_anchor.xml":
            goobiSSH.downloadFile(f"{remote_dir}{metaFile}",  f"{dlza.dlzaDirs['metadata']}{metaFile}")

    #Write mets.xml File to metadata-Directory
    if metsFile != None:
        tree = etree.ElementTree(metsFile)
        with open(f"{dlza.dlzaDirs['metadata']}{recordId}_mets.xml", "wb") as f:
            tree.write(f, encoding="UTF-8", xml_declaration=True, pretty_print=True)
        

    #Check if ZentralGut-Process depends on Alma:
    mmsidPattern = r"^9[\d]+[05$|01$]"
    mmsidMatch = re.match(mmsidPattern, zentralGutId[0]["value"])
    if mmsidMatch:
        #print(f'\t{zentralGutId[0]["value"]} matches with ALMA-Pattern: {str(bool(match))}')
        mmsID = mmsidMatch.group()
        mmsIDs = alma.getNormalizedMMSIDs(mmsID)

        marcRecord = alma.getBibRecord(mmsIDs["IZ_MMSID"])
        tree = etree.ElementTree(etree.fromstring(marcRecord["bib"][0]["anies"][0]))
        with open(f"{dlza.dlzaDirs['metadata']}{mmsIDs['IZ_MMSID']}.marcxml", "wb") as f:
            tree.write(f, encoding="UTF-8", xml_declaration=True, pretty_print=True)
    
    #Download Ruleset.xml as additional file for Goobi appropriate transformation
    rulesetFile = config.goobi_rulesets[processData["rulesetName"]]
    goobiSSH.downloadFile(f"{remote_dirRuleSet}{rulesetFile}",  f"{dlza.dlzaDirs['metadata']}{rulesetFile}")

    # Zu CompleteSet hinzufügen
    completeSet.append(infoSet.copy())
    
    # Write the infoSet to a JSON file
    dlza.writeInfoSetJson(infoSet)

    #Download Files (Master-Images and if given: Import-File, alto.xml, ocr-plain.txt, splitted-pdf)
    if config.downloadFiles == True:
        s3Prefixes = [f"{recordId}/images/{processData['title']}_master/", 
                      f"{recordId}/import/", 
                      f"{recordId}/ocr/{processData['title']}_alto/", 
                      f"{recordId}/ocr/{processData['title']}_txt/", 
                      f"{recordId}/ocr/{processData['title']}_pdf/" ]
        for s3Prefix in s3Prefixes:
            response = s3Conn.s3.list_objects_v2(Bucket=s3Conn.bucket, Prefix=s3Prefix)
            for obj in response.get('Contents', []):
                #print(obj['Key'])
                fileName = re.sub(response["Prefix"],"",obj["Key"])
                localPath = f"{dlza.dlzaDirs['data']}{fileName}"
                s3Conn.s3.download_file(s3Conn.bucket, obj['Key'], localPath)
                logger.log(f"✅ Downloaded { obj['Key']} → {localPath}")
        
    # create zip-file of SIP-direcotry
    if config.zipFiles == True:
        dlza.zip_directory(dlza.dlzaDirs["recordDir"], f"{baseDir}{collection}/{foldername}.zip", rmSourceDir=config.remove_collection_folder_after_zipping)
    
    #Log Finishing of current record
    logger.log(f"🎯 Finished record no. {str(i+1).zfill(4)} with ID: {recordId} at {datetime.now().isoformat()}")
    logger.log(f"==============================================================")

# Writing completeSet as json file
dlza.writeCompleteSet(completeSet, fulljsonfile)
df_json = pd.read_json(fulljsonfile)
df_json.to_excel(fullexcelfile)
logger.log(f"🎯 Total records: {i+1}\nStarted ad {now} - Finished at {datetime.now().isoformat()}")
logger.log(f"==============================================================")
logger.log(f"==============================================================")