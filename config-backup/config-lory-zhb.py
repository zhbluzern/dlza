# collection: 
# not allowed: characters ~ “ # % & * : < > ? / \ { | }

collection_id = 'lory_zhb'
collection = 'Lory ZHB-Community'
ingest_workflow = 'zenodo' 
keywords = []  # array
sets = ['zhb', 'lory', 'lory_zhb', 'zenodo', 'all', 'digitalborn', 'openscience'] # array
input_file = 'lory_zhb.xlsx'


# metadata formats: 

marcxml = 'False'
mets = 'False'
mods = 'False'
datacite = 'True'
dc = 'True'
zenodomarc = 'True'
zenodoapi = 'True'
tei = 'True'

# user information 

user_name = 'Kathrin Heim <kathrin.heim@zhbluzern.ch>'
user_address = 'mailto:dlza@zhbluzern.ch'
user_root = 'G:/Research10/ZHB-DLZA/dlza'

# organisation information

organisation = 'Zentral- und Hochschulbibliothek Luzern'
organisation_id = 'zhb'
organisation_address = 'mailto:info@zhbluzern.ch'


# DLZA Workbench information

dlza_root = 'D:/Ingest'
gocfl_conf = 'D:/Ingest/config/zhb-config.toml'
gocfl = 'gocfl'
ona_conf = 'D:/Ingest/config/ona-config.yml'

# general configuration

baseurl_doi = 'https://doi.org/' # DOI baseurl
baseurl_alma = 'https://rzs.swisscovery.slsp.ch/permalink/41SLSP_RZS/ldslj8/alma' # Base URL for your Library catalogue permalink
baseurl_marc = 'https://slsp-rzs.alma.exlibrisgroup.com/view/sru/41SLSP_RZS?version=1.2&operation=searchRetrieve&recordSchema=marcxml&query=rec.id=' # MARC: Alma SRU Base URL, change your institution zone and code
baseurl_mods = 'https://slsp-rzs.alma.exlibrisgroup.com/view/sru/41SLSP_RZS?version=1.2&operation=searchRetrieve&recordSchema=mods&query=rec.id=' #MODS: Alma SRU  Base URL, change your institution zone and code
baseurl_zenodo_oai = 'https://zenodo.org/oai2d' # OAI-PMH url
baseurl_zenodo_api = 'https://zenodo.org/api/records' # for api export
baseurl_tei = 'https://www.e-codices.unifr.ch/xml/tei_published' # TEI: Baseurl for ecodices tei format
baseurl_mets = 'https://www.e-manuscripta.ch/oai?'
