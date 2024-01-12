# collection: 
# not allowed: characters ~ “ # % & * : < > ? / \ { | }

collection_id = 'lory_unilu'
collection = 'LORY Universität Luzern'
ingest_workflow = 'zenodo' 
keywords = []  # array
sets = ['unilu', 'zhb', 'lory', 'lory_unilu'] # array
input_file = 'lory_unilu.xlsx'
inventory_file = 'lory_unilu_inventory.json'
inventory_xlsx = 'lory_unilu_inventory.xlsx'


# metadata formats

marcxml = 'False'
marcxml_baseurl = 'https://slsp-rzs.alma.exlibrisgroup.com/view/sru/41SLSP_RZS?version=1.2&operation=searchRetrieve&recordSchema=marcxml&query=rec.id='

datacite = 'True'
dc = 'True'
zenodo_set = 'user-lory_unilu' # OAI set name, eg. user-lory
zenodo_baseurl = 'https://zenodo.org/oai2d'


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

