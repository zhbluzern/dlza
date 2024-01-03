# collection: not allowed: characters ~ “ # % & * : < > ? / \ { | }

collection_id = 'sosa_emanus'
collection = 'ZHB Sosa E-Manuscripta'
ingest_workflow = 'e-manuscripta' 
keywords = ['E-Manuscripta', 'ZHB', 'Sondersammlung']  # array
sets = ['e-manuscripta', 'zhb', 'sosa', 'lara'] # array
input_file = 'e-manuscripta.xlsx'


# metadata formats for this collection

marcxml = 'true'
marcxml_baseurl = 'https://slsp-rzs.alma.exlibrisgroup.com/view/sru/41SLSP_RZS?version=1.2&operation=searchRetrieve&recordSchema=marcxml&query=rec.id='

datacite = 'false'
datacite_set = 'user-lara' # OAI set name, eg. user-lory, user-lara...
datacite_baseurl = 'https://zenodo.org/oai2d'


# user information 

user_name = 'Kathrin Heim'
user_address = 'mailto:lit@zhbluzern.ch'
user_root = "C:/Users/HeimK/switchdrive/jupyter/dlza"


# organisation information

organisation = 'Zentral- und Hochschulbibliothek Luzern'
organisation_id = 'zhb'
organisation_address = 'mailto:lit@zhbluzern.ch'


# DLZA Workbench information

dlza_root = 'D:/Ingest'
gocfl_conf = 'D:/Ingest/config/zhb-config.toml'
gocfl = 'gocfl.exe'


# general configuration

baseurl_doi = 'https://doi.org/'
baseurl_alma = 'https://rzs.swisscovery.slsp.ch/permalink/41SLSP_RZS/ldslj8/alma'


# subdirectories 

files_path = 'files'
metadata_path = 'metadata'
object_path = 'objects'
info_path = 'info'

