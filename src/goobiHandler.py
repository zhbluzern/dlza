import requests
import os
from dotenv import load_dotenv
from lxml import etree

class goobiHandler:
    def __init__(self):
        load_dotenv()
        self.apiToken = os.getenv("apiToken")
        self.apiUrl = os.getenv("goobiApiUrl")
        self.sourceFileUrl = os.getenv("goobiSourceFileUrl")
        self.namespaces = { "xmlns" : "http://www.openarchives.org/OAI/2.0/", "mods":"http://www.loc.gov/mods/v3", "mets" : "http://www.loc.gov/METS/", "xlink":"http://www.w3.org/1999/xlink"}

    #This Method is loading the exported METS-SourceFile from the Viewer
    def getSourceFile(self, CatalogIDDigital):
        result = requests.get(url=f"{self.sourceFileUrl}{CatalogIDDigital}", headers = {"accept":"*/*", "Content-Type" : "application/xml"})
        #return (result.content)
        metsTree = etree.fromstring(result.content)
        return metsTree

    def getSourceFileUrl(self, CatalogIDDigital):
        return f"{self.sourceFileUrl}{CatalogIDDigital}"
    
    # Start of Workflow-API-Methods
    def getJournal(self, processId):
        result = requests.get(url=f"{self.apiUrl}process/{processId}/journal", headers={"accept":"*/*", "token": self.apiToken})
        print(result.json())

    def writeJournal(self, processId, journalMessage, journalType="info"):
        journalData = { "type": journalType, "message": journalMessage}
        result = requests.post(url=f"{self.apiUrl}process/{processId}/journal", 
                            headers={"accept":"*/*", "token": self.apiToken, "Content-Type" : "application/json"},
                            json=journalData)
        print(result.text)

    def createProcess(self, processData):
        result = requests.post(url=f"{self.apiUrl}process/", 
                            headers={"accept":"*/*", "token": self.apiToken, "Content-Type" : "application/json"},
                            json=processData)
        return (result.text)
    
    def createProcessByOpac(self, processData):
        result = requests.post(url=f"{self.apiUrl}processes/", 
                            headers={"accept":"*/*", "token": self.apiToken, "Content-Type" : "application/json"},
                            json=processData)
        return (result.text)   
    def updateProcess(self, processData):
        result = requests.post(url=f"{self.apiUrl}process/", 
                            headers={"accept":"*/*", "token": self.apiToken, "Content-Type" : "application/json"},
                            json=processData)
        return (result.text)
    
    def queryWorkflow(self, filterObject):
        result = requests.put(url=f"{self.apiUrl}process/query",
                              headers={"accept":"*/*", "token": self.apiToken, "Content-Type" : "application/json"},
                              json=filterObject)
        #print(result.text)
        return(result.json())
    
    def getProcess(self, processId):
        result = requests.get(url=f"{self.apiUrl}process/{processId}",
                              headers={"accept":"*/*", "token": self.apiToken, "Content-Type" : "application/json"})
        return result.json()

    def addMetadata(self, processId, metadataObject):
        result = requests.post(url=f"{self.apiUrl}process/{processId}/metadata",
                              headers={"accept":"*/*", "token": self.apiToken, "Content-Type" : "application/json"},
                              json=metadataObject)
        return (result.text)
    
    def updateMetadata(self, processId, metadataObject):
        result = requests.put(url=f"{self.apiUrl}process/{processId}/metadata",
                              headers={"accept":"*/*", "token": self.apiToken, "Content-Type" : "application/json"},
                              json=metadataObject)
        return (result.text)        
    def removeMetadata(self, processId, metadataObject):
        result = requests.delete(url=f"{self.apiUrl}process/{processId}/metadata",
                              headers={"accept":"*/*", "token": self.apiToken, "Content-Type" : "application/json"},
                              json=metadataObject)
        return (result.text)
    
    def getMetadata(self, processId):
        result = requests.get(url=f"{self.apiUrl}process/{processId}/metadata",
                              headers={"accept":"*/*", "token": self.apiToken, "Content-Type" : "application/json"})
        return result.json()

    def getMetadataDetail(self, metadata, metadataNames, metadataLevel="topstruct", metadataValue=""):
        result = list(filter(lambda d: d["name"] in metadataNames and  (metadataLevel == "" or d.get("metadataLevel") == metadataLevel),
        metadata))
        return result
    
    def closeStep(self, processId, stepName):
        result = requests.put(url=f"{self.apiUrl}process/{processId}/step/close",
                              headers={"accept":"*/*", "token": self.apiToken, "Content-Type" : "application/json"},
                              json = {"stepname":stepName})
        return (result.text)
    
    def createByMARC(self, projectName, templateName, processTitle):
        result = requests.post(url=f"{self.apiUrl}metadata/marc/{projectName}/{templateName}/{processTitle}",
                               headers={"accept":"*/*", "token": self.apiToken, "Content-Type" : "application/json"})
        return (result.text)
    
    def getSteps(self, processId):
        result = requests.get(url=f"{self.apiUrl}process/{processId}/steps",
                              headers={"accept":"*/*", "token": self.apiToken, "Content-Type" : "application/json"})
        return result.json()
    

if __name__ == "__main__":
    goobi = goobiHandler()
    # metadata = goobi.getMetadata("10643")
    # zentralGutId = goobi.getMetadataDetail(metadata,metadataNames=["CatalogIDDigital"])
    # ark = goobi.getMetadataDetail(metadata,metadataNames=["ARK"])
    # title = goobi.getMetadataDetail(metadata,metadataNames=["TitleDocMain"],metadataLevel="")
    # license = goobi.getMetadataDetail(metadata,metadataNames=["UseAndReproductionLicense"])
    # print(title)

    process = goobi.getProcess("10643")
    goobi_rulesets = { "LU222": "ruleset_LU222.xml",   "newspaper": "newspaper.xml",   "Regelsatz Newspaper": "ruleset_newspaper.xml",   "Standard": "ruleset.xml" }
    print(f'Ruleset {process["rulesetName"]} has file: {goobi_rulesets[process["rulesetName"]]}')
