# collection: 

collection_id = 'emanus'
collection = 'ZHB Sosa E-Manuscripta'
zenodo_set = 'user-zenodo' # Zenodo OAI set name, eg. user-lory
ingest_workflow = 'e-manuscripta' 
keywords = []  # array
sets = ['e-manuscripta', 'zhb', 'sosa', 'all', 'digitalisat', 'alma'] # array
input_file = 'e-manuscripta.xlsx'

# metadata formats: 

marcxml = 'True'
mets = 'False'
mods = 'False'
datacite = 'False'
dc = 'False'
apidata = 'False'
tei = 'False'

# user information 

user_name = 'name of ingester <email@inst.org>'
user_address = 'mailto:dlza@zhbluzern.ch'
user_root = 'C:/temp/dlza'

# organisation information

organisation = 'Zentral- und Hochschulbibliothek Luzern'
organisation_id = 'zhb'
organisation_address = 'mailto:info@inst.org'


# DLZA Workbench information

dlza_root = 'E:/Ingest'
gocfl_conf = 'D:/Config/zhb-config.toml'
gocfl = 'gocfl'
ona_conf = 'D:/Config/ona-config.yml'

# general configuration

baseurl_doi = 'https://doi.org/' # DOI baseurl
baseurl_alma = 'https://rzs.swisscovery.slsp.ch/permalink/41SLSP_RZS/ldslj8/alma' # Base URL for your Library catalogue permalink
baseurl_marc = 'https://slsp-rzs.alma.exlibrisgroup.com/view/sru/41SLSP_RZS?version=1.2&operation=searchRetrieve&recordSchema=marcxml&query=rec.id=' # Alma SRU Base URL, change your institution zone and code
baseurl_zenodo_oai = 'https://zenodo.org/oai2d' # OAI-PMH url
baseurl_zenodo_api = 'https://zenodo.org/api/records' # for api export
baseurl_ecodices = 'https://www.e-codices.unifr.ch/xml/tei_published' # for tei format

