# collection: 
# not allowed: characters ~ “ # % & * : < > ? / \ { | }

collection_id = 'emanus'
collection = 'ZHB Sosa E-Manuscripta'
ingest_workflow = 'e-manuscripta' 
keywords = []  # array
sets = ['e-manuscripta', 'zhb'] # array
input_file = 'e-manuscripta.xlsx'
inventory_file = 'e-manuscripta_inventory.json'
inventory_xlsx = 'e-manuscripta_inventory.xlsx'

# metadata formats

marcxml = 'True'
datacite = 'False'
dc = 'False'
apidata = 'False'
tei = 'False'

# metadata base urls

marcxml_baseurl = 'https://slsp-rzs.alma.exlibrisgroup.com/view/sru/41SLSP_RZS?version=1.2&operation=searchRetrieve&recordSchema=marcxml&query=rec.id=' # Alma SRU Base URL, change your institution zone and code

zenodo_baseurl = 'https://zenodo.org/oai2d'
zenodo_set = 'user-lory' # Zenodo OAI set name, eg. user-lory
zenodo_api = 'https://zenodo.org/api/records'

ecodices_url = 'https://www.e-codices.unifr.ch/xml/tei_published' # for tei format

# user information 

user_name = 'Vorname Nachname'
user_address = 'mailto:vorname.nachname@myinstitution.ch'
user_root = "C:/temp"

# organisation information

organisation = 'Zentral- und Hochschulbibliothek Luzern'
organisation_id = 'zhb'
organisation_address = 'mailto:organisation@myinstitution.ch'


# DLZA Workbench information

dlza_root = 'D:/Ingest'
gocfl_conf = 'config.toml'
gocfl = 'gocfl'

# general configuration

baseurl_doi = 'https://doi.org/'
baseurl_alma = 'https://rzs.swisscovery.slsp.ch/permalink/41SLSP_RZS/ldslj8/alma' # Base URL for your Library catalogue permalink

# subdirectories 

info_path = 'info'
metadata_path = 'metadata'
object_path = 'objects'
gocfl_path = 'gocfl'

