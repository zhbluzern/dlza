from datetime import datetime
# collection: 

collection_id = 'zentralgut'
collection = 'ZHB ZentralGut'
zenodo_set = 'user-lara' # Zenodo OAI set name, eg. user-lory
zentralgut_oai_sets = ["DC:zentralundhochschulbibliothekluzern.portraitgalerie"]
#zentralgut_filter = ["meta:singleDigCollection:Zentral- und Hochschulbibliothek Luzern#Portraitgalerie"]
zentralgut_filter = ["ID:10946 10947 10945 10643 2623"]
goobi_rulesets = { "LU222": "ruleset_LU222.xml",   "newspaper": "newspaper.xml",   "Regelsatz Newspaper": "ruleset_newspaper.xml",   "Standard": "ruleset.xml" }
input_file = ''
downloadFiles = True
remove_collection_folder_after_zipping = True
ingest_workflow = 'zentralgut' 
boilerplate = "boilerplate/" #a subdirectory for working on creating inventory, loading data, zipping them etc. even empty, script runs entirely in root of the script.
keywords = []  # array
#sets = ['e-codices', 'zhb', 'sosa', 'all', 'digitalisat', 'alma'] # array
sets = ["zentralgut"]


# metadata formats: 
marcxml = 'True'
mets = 'True'
mods = 'False'
datacite = 'True'
dc = 'False'
zenodomarc = 'False'
zenodoapi = 'False'
tei = 'False'
goobi = 'True'

# user information 

user_name = 'Kathrin Heim <kathrin.heim@zhbluzern.ch>'
user_address = 'mailto:dlza@zhbluzern.ch'
user_root = 'G:/Research10/ZHB-DLZA/dlza'

# organisation information

organisation = 'Zentral- und Hochschulbibliothek Luzern'
organisation_id = 'zhb'
organisation_address = 'mailto:info@zhbluzern.ch'


# DLZA Workbench information

dlza_root = 'E:/Ingest'
gocfl_conf = 'D:/Config/zhb-config.toml'
gocfl = 'gocfl'
ona_conf = 'D:/Config/ona-config.yml'

# general configuration

baseurl_doi = 'https://doi.org/' # DOI baseurl
baseurl_alma = 'https://rzs.swisscovery.slsp.ch/permalink/41SLSP_RZS/ldslj8/alma' # Base URL for your Library catalogue permalink
baseurl_marc = 'https://slsp-rzs.alma.exlibrisgroup.com/view/sru/41SLSP_RZS?version=1.2&operation=searchRetrieve&recordSchema=marcxml&query=rec.id=' # MARC: Alma SRU Base URL, change your institution zone and code
baseurl_mods = 'https://slsp-rzs.alma.exlibrisgroup.com/view/sru/41SLSP_RZS?version=1.2&operation=searchRetrieve&recordSchema=mods&query=rec.id=' #MODS: Alma SRU  Base URL, change your institution zone and code
baseurl_zenodo_oai = 'https://zenodo.org/oai2d' # OAI-PMH url
baseurl_zenodo_api = 'https://zenodo.org/api/records' # for api export
baseurl_tei = 'https://www.e-codices.unifr.ch/xml/tei_published' # TEI: Baseurl for ecodices tei format
baseurl_mets = 'https://www.e-manuscripta.ch/oai?'
baseurl_zentralgut_oai = "https://zentralgut.ch/oai"

# default InfoSet
def loadInfoSet(nowTimeStamp=datetime.now().isoformat()):
    infoSet = { 
    # infoset created after https://github.com/je4/gocfl/blob/main/gocfl-info-1.0.json 

    "signature": "",
    "organisation_id": organisation_id,
    "organisation": organisation,
    "organisation_address": organisation_address,
    "collection_id": collection_id,
    "collection": collection,
    "sets": sets,
    "identifiers": [],
    "title": "",
    "alternative_titles": [],
    "description": "",
    "keywords": keywords,
    "user": user_name,
    "address": user_address,
    "created": nowTimeStamp,
    "last_changed": nowTimeStamp,
    "deprecates": "",
    "references": "",
    "ingest_workflow": ingest_workflow,
    "additional": []
    }
    return infoSet

if __name__ == "__main__":
    print(loadInfoSet())