# collection: 
# not allowed: characters ~ “ # % & * : < > ? / \ { | }

collection_id = 'sosa_ecod'
collection = 'ZHB Sosa E-Codices'
ingest_workflow = 'e-codices' 
keywords = []  # array
sets = ['e-codices', 'zhb', 'sosa', 'lara'] # array
input_file = 'e-codices.xlsx'
inventory_file = 'e-codices_inventory.json'
inventory_xlsx = 'e-codices_inventory.xlsx'

# metadata formats
# alma
marcxml = 'True'
marcxml_baseurl = 'https://slsp-rzs.alma.exlibrisgroup.com/view/sru/41SLSP_RZS?version=1.2&operation=searchRetrieve&recordSchema=marcxml&query=rec.id='
# zenodo
datacite = 'False'
dc = 'False'
apidata = 'False'
zenodo_baseurl = 'https://zenodo.org/oai2d'
zenodo_api = 'https://zenodo.org/api/records'

# ecodices
tei = 'True'
ecodices_url = 'https://www.e-codices.unifr.ch/xml/tei_published'

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

