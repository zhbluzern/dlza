import urllib.request
from lxml import etree
import config
import pandas as pd

# SRU base and namespaces:
sru = config.baseurl_marc
ns = {'xmlns' : 'http://www.loc.gov/zing/srw/', 
  'slim' : 'http://www.loc.gov/MARC21/slim'}  

# other variables
input_file = config.input_file


def getBibFromSRU(recid, ns, sru):
    sruUrl = sru+recid
    #print(sruUrl)
    #Initial SRU-Request        
    root = etree.parse(urllib.request.urlopen(sruUrl))
    #Initial xpath to parse the first  records
    record = root.findall(".//xmlns:record",ns)

    #Get the nextRecordValue to build the further SRU-Requests with additional startRecord URI-Parameter
    nextRecord = root.find(".//xmlns:nextRecordPosition",ns)
    
    return record

def get_nz_id(record, ns):
    for rec in record:
        resultDet= {}

        slspNetworkId = rec.xpath(".//slim:datafield[@tag='035']/slim:subfield[@code='a'][starts-with(text(),'(EXLNZ-41SLSP_NETWORK)')]",namespaces=ns)
        network_id = slspNetworkId[0].text[22:]

        return network_id
    
# Read the Excel file into a pandas DataFrame
df = pd.read_excel(input_file)
df['MMS ID'] = df['MMS ID'].astype(str)
df["Network ID"] = None

for idx, row in df.iterrows():

    mms_id = row['MMS ID']
    sruRecord = getBibFromSRU(mms_id, ns, sru)
    nz_id = get_nz_id(sruRecord, ns)
    print(nz_id)
    df.loc[idx, 'Network ID'] = nz_id


#print(df)
df.to_excel(input_file, index=False)
print("Datei gespeichert als:", input_file)
