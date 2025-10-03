import requests
from lxml import etree
import pandas as pd
import json
# if __name__ == '__main__':
#     import readAllMods as mods
# else:
#     import src.readAllMods as mods

def harvestOai(oaiUrl, oaiParams, outputFileName):
    params = oaiParams
    headers = {"Accept": "application/xml"}
    namespaces = { "xmlns" : "http://www.openarchives.org/OAI/2.0/", "mods":"http://www.loc.gov/mods/v3", "mets" : "http://www.loc.gov/METS/", "xlink":"http://www.w3.org/1999/xlink"}

    r = requests.get(oaiUrl, headers=headers, params=params)
    root = etree.fromstring(r.content)

    ListRecords = root.xpath(".//xmlns:ListRecords", namespaces=namespaces)
    #print(ListRecord[0].getchildren())
    records = root.xpath(".//xmlns:record", namespaces=namespaces)
    resumToken = root.xpath(".//xmlns:resumptionToken", namespaces=namespaces)
    resumCount = 0
    noR = int(resumToken[0].get('completeListSize'))
    recordCount = 0
    resultSet = []

    while recordCount < noR:
        
        for i, record in enumerate(records):
            metadata = record.xpath(".//xmlns:metadata", namespaces=namespaces)
            recordCount += 1
            print(f"#{recordCount} - {metadata[0].getchildren()}")
            resultDet = metadata
            resultSet.append(resultDet)
            #add record to root element
            if resumCount > 0:
                ListRecords[0].append(record)

        if resumToken != []:
            resumCount += 1
            nextRecords = requests.get(oaiUrl, headers=headers, params={"verb":params["verb"], "resumptionToken":resumToken[0].text})
            nextRecordsRoot = etree.fromstring(nextRecords.content)
            records = nextRecordsRoot.xpath(".//xmlns:record", namespaces=namespaces)
            resumToken = nextRecordsRoot.xpath(".//xmlns:resumptionToken", namespaces=namespaces)

        if resumToken != []:
            print(f"Current Cursor: {resumToken[0].get('cursor')}/{resumToken[0].get('completeListSize')}. Resume: {resumToken[0].text}")

    #Prepare for and write full METS-XML-Dump (remove ResumptionToken)
    fullMets = etree.ElementTree(root)
    resumTokens = fullMets.xpath(".//xmlns:resumptionToken", namespaces=namespaces)
    for resumToken in resumTokens:
        print(resumToken)
        resumToken.getparent().remove(resumToken)
    fullMets.write(f'boilerplate/{outputFileName}.xml',encoding="UTF-8", xml_declaration=True, pretty_print=True)

    df = pd.DataFrame(resultSet) 
    df.to_csv(f'boilerplate/{outputFileName}.csv', index=False)

    with open(f"boilerplate/{outputFileName}.json", "w") as jsonFile:
        jsonFile.write(json.dumps(resultSet, indent=2))

