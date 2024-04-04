# collection: 
# not allowed: characters ~ “ # % & * : < > ? / \ { | }

collection_id = 'lory_zhb'
collection = 'LORY ZHB-Collection'
ingest_workflow = 'zenodo' 
keywords = []  # array
sets = ['zhb', 'lory', 'lory_zhb'] # array
input_file = 'lory_zhb.xlsx'
inventory_file = 'lory_zhb_inventory.json'
inventory_xlsx = 'lory_zhb_inventory.xlsx'


# metadata formats

marcxml = 'False'
marcxml_baseurl = 'https://slsp-rzs.alma.exlibrisgroup.com/view/sru/41SLSP_RZS?version=1.2&operation=searchRetrieve&recordSchema=marcxml&query=rec.id='

datacite = 'True'
dc = 'True'
apidata = 'True'
zenodo_set = 'user-lory_zhb' # OAI set name, eg. user-lory
zenodo_baseurl = 'https://zenodo.org/oai2d'
zenodo_api = 'https://zenodo.org/api/records'


# user information 

user_name = 'Kathrin Heim'
user_address = 'mailto:kathrin.heim@zhbluzern.ch'
user_root = "C:/Users/HeimK/switchdrive/jupyter/dlza"


# organisation information

organisation = 'Zentral- und Hochschulbibliothek Luzern'
organisation_id = 'zhb'
organisation_address = 'mailto:lit@zhbluzern.ch'


# DLZA Workbench information

dlza_root = 'D:/Ingest'
gocfl_conf = 'D:/Ingest/config/zhb-config.toml'
#gocfl = 'gocfl.exe'
gocfl = 'gocfl'


# general configuration

baseurl_doi = 'https://doi.org/'
baseurl_alma = 'https://rzs.swisscovery.slsp.ch/permalink/41SLSP_RZS/ldslj8/alma'


# subdirectories 

info_path = 'info'
metadata_path = 'metadata'
object_path = 'objects'
gocfl_path = 'gocfl'

