import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

## Class to handle with the ExL-Bibliographics-API to handle some portfolio related calls
class ExL_Bib:

    # Initialisiere ExLibris-Portfolio Klasse für weitere API-Calls
    def __init__(self, apiKey=""):
        if apiKey != "":
            self.apiKey = apiKey
        else:
            self.apiKey = os.getenv("almaApiKey")
        self.headers = {"Accept": "application/json"}
        self.params = {'apikey': self.apiKey, "view":"full", "expand":"None"}
        self.apiUrl = "https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs"

    def getBibRecord(self, mmsID):
        params = self.params
        params.update({"mms_id":mmsID})
        response = requests.get(url=self.apiUrl, params=params, headers=self.headers)
        return response.json()
    
    # Method getNormalizedMMSIDs checks whether a given MMS-ID is an NZ or an IZ-ID (or nothing) and returns an object with both mms-ids
    def getNormalizedMMSIDs(self, mmsID):
        result={}
        # 1. Check if mmsID is NZ-ID
        isNzId = self.checkIfIsNzId(mmsID)
        # 1.a If 1 = true
        if isNzId == True:
            result["NZ_MMSID"] = mmsID
            result["IZ_MMSID"] = self.checkMMSIdisNZId(mmsID)

        # 1.b If 1 == False
        else:
            isIzId = self.checkMMSIdisIZId(mmsID)
            #print(isIzId)
            if isIzId == True:
                result["NZ_MMSID"] = self.getNZId(mmsID)
                result["IZ_MMSID"] = mmsID
            
            # 2.b if iz-id == false (bedeutet auch dass gegebene mmsId weder iz noch nz mms-id ist - ein fehler in der id liegt vor)
            else:
                result = None

        return result

    # checks if a mms-id is a nz-id, returns Boolean
    def checkIfIsNzId(self, mmsId):
        thisParams = self.params.copy()
        thisParams.update({"nz_mms_id": mmsId})
        r = requests.get(f"{self.apiUrl}",
                                params=thisParams,
                                headers=self.headers)
        thisParams.clear()

        result = r.json()
        #print(result)
        if result.get("errorsExist"):
            return False
        else:
            return True
        
    def checkIfIsIzId(self, mmsId):
        thisParams = self.params.copy()
        thisParams.update({"mms_id": mmsId})
        r = requests.get(f"{self.apiUrl}",
                                params=thisParams,
                                headers=self.headers)
        thisParams.clear()
        result = r.json()

        if result.get("errorsExist"):
            return False
        elif result["bib"] != [] and result["bib"][0]["mms_id"] == mmsId:
            return True
        
    # Check if mmsId is NZ Id and returns the local IZ mms id for portfolio creation
    def checkMMSIdisNZId(self, mmsId):
        thisParams = self.params.copy()
        thisParams.update({"nz_mms_id": mmsId})
        r = requests.get(f"{self.apiUrl}",
                                params=thisParams,
                                headers=self.headers)
        result = r.json()
        thisParams.clear()
        if result.get("errorsExist") and result["errorsExist"] == "True":
            return "Error"
        else:
            try: 
                return result["bib"][0]["mms_id"]
            except:
                return None

    #Method getNZId returns the NZ-MMSID for a given IZ-ID
    def getNZId(self, mmsId):
        thisParams = self.params.copy()
        thisParams.update({"mms_id": mmsId})
        r = requests.get(f"{self.apiUrl}",
                                params=thisParams,
                                headers=self.headers)
        result = r.json()
        #print(f'{result["bib"][0]["mms_id"]} == {mmsId}?')
        thisParams.clear()
        
        if result.get("errorsExist") and result["errorsExist"] == "True":
            return "Error"
        if result["bib"][0]["mms_id"] == str(mmsId):
            return result["bib"][0]["linked_record_id"]["value"]
            
    # Check if an IZ MMS ID is given, returns True if it is a IZ id, returns "Error" on Error
    def checkMMSIdisIZId(self, mmsId):
        thisParams = self.params
        thisParams.update({"mms_id": mmsId})
        r = requests.get(f"{self.apiUrl}",
                                params=thisParams,
                                headers=self.headers)
        result = r.json()
        
        #print(result["bib"])
        if result.get("errorsExist") and result["errorsExist"] == "True":
            return "Error"
        else:
            try: 
                if result["bib"][0]["mms_id"] == mmsId:
                    return True
                else:
                    return False
            except:
                return None

if __name__ == "__main__":
    alma = ExL_Bib()
    # result = alma.getBibRecord("9914349641505505")
    from lxml import etree
    import re

    result = alma.getNormalizedMMSIDs("991820170105505")
    print(result)
    marcRecord = alma.getBibRecord(result["IZ_MMSID"])
    print(marcRecord["bib"][0]["anies"][0])

    tree = etree.ElementTree(etree.fromstring(marcRecord["bib"][0]["anies"][0]))
    with open(f"boilerplate/zentralgut/test_alma.marcxml", "wb") as f:
        tree.write(f, encoding="UTF-8", xml_declaration=True, pretty_print=True)    

    # marcXml = etree.fromstring(result["bib"][0]["anies"][0])
    # print(marcXml)
    # urls = marcXml.xpath(".//datafield[@tag='856']")
    # resultDet = {}
    # if urls != []:
    #     for index,url in enumerate(urls):
    #         uri = url.xpath(".//subfield[@code='u']") 
    #         uriText = url.xpath(".//subfield[@code='3']")
    #         if uriText != []:
    #             normalizedColName = re.sub(r'[\.\s]','',uriText[0].text)
    #             uriColumn = f"url_{normalizedColName}"
    #         if resultDet.get(uriColumn):
    #             uriColumn = f"{uriColumn}_{index}"
    #         print(f"{uriColumn}: {uri[0].text}")
    #         resultDet[uriColumn] = uri[0].text
    
    # print(resultDet)