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

marcxml = 'True'
datacite = 'False'
dc = 'False'
apidata = 'False'
tei = 'True'

# metadata base urls

marcxml_baseurl = 'https://slsp-rzs.alma.exlibrisgroup.com/view/sru/41SLSP_RZS?version=1.2&operation=searchRetrieve&recordSchema=marcxml&query=rec.id='

zenodo_baseurl = 'https://zenodo.org/oai2d'
zenodo_set = 'user-lory_zhb' # OAI set name, eg. user-lory
zenodo_api = 'https://zenodo.org/api/records'

ecodices_url = 'https://www.e-codices.unifr.ch/xml/tei_published' # for tei format


# user information 

user_name = 'Kathrin Heim'
user_address = 'mailto:kathrin.heim@zhbluzern.ch'
user_root = "G:/Research10/ZHB-DLZA/dlza-main"


# organisation information

organisation = 'Zentral- und Hochschulbibliothek Luzern'
organisation_id = 'zhb'
organisation_address = 'mailto:lit@zhbluzern.ch'


# DLZA Workbench information

dlza_root = 'D:/Ingest'
gocfl_conf = 'D:/Ingest/config/zhb-config.toml'
gocfl = 'gocfl'

# general configuration

baseurl_doi = 'https://doi.org/'
baseurl_alma = 'https://rzs.swisscovery.slsp.ch/permalink/41SLSP_RZS/ldslj8/alma'


# subdirectories 

info_path = 'info'
metadata_path = 'metadata'
object_path = 'objects'
gocfl_path = 'gocfl'

