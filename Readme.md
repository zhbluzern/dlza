# Readme DLZA @ zhbluzern

Diese Jupyter Notebooks dienen zur Aufbereitung der Datenobjekte und Metadaten aus den Beständen der ZHB Luzern für die digitale Langzeitarchivierung (DLZA) der ZHB Luzern, basierend auf der GOCFL implementierung von Jürgen Enge, https://github.com/je4/gocfl .

Es werden Bestände der Sondersammlung (E-Rara, E-codices, etc.), aus dem Open-Science-Repositories (Lory, Lara) sowie weiteren Sammlungen aufbereitet. Für jede Sammlung (= collection) gibt es ein eigenes Jupyter Notebook, aber folgende Grundlagen gelten für alle:



## Basiskonfiguration

Es wird eine info.json Datei nach folgendem Schema erstellt:
https://github.com/je4/gocfl/blob/main/gocfl-info-1.0.json 

Vereinfacht gesagt, muss eine info.json folgendermassen aussehen: 

    infoSet = {
        'additional': '',
        'address': config.address, 
        'collection': config.collection,
        'collection_id': config.collection_id,
        'created': 'yyyy-mm-dd'
        'description': '',
        'identifiers': [],
        'ingest_workflow': config.ingest_workflow, 
        'keywords': config.keywords, 
        'last_changed': config.last_changed,
        'organisation' : config.organisation,
        'organisation_id' : config.organisation_id, 
        'references' : [],
        'sets' : config.sets,
        'signature': '', 
        'title' : '', 
        'user' : ''       
    }

Pflichtfelder sind: "signature", "organisation_id", "organisation", "title", "user", "address", "created", "last_changed".

Die Signature ist die zentrale ID für die Erstellung der Archivkapseln und besteht daher aus einem dauerhaften Identifier (bspw. DOI). 

Im Config-File wird die Abteilung (bspw. zhb_...) hinzugefügt, das Script ergänzt den Identifier. 


### Config.py

Die config.py beinhaltet diverse Daten, welche nicht aus den bestehenden Metadaten (Schnittstelle) kommen, und kann pro Set konfiguriert werden (z.B. author, institution, etc.). Sie muss in folgender Struktur vorliegen (Beispieldaten für ZHB E-Rara)

    address = 'mailto:someone@internet.com'
    collection = 'ZHB E-Rara'
    collection_id = 'zhb_erara'
    ingest_workflow = 'W01'
    keywords = '[E-Rara, ZHB, Sondersammlung]'
    last_changed = '2023-07-27'
    organisation = 'Zentral- und Hochschulbibliothek Luzern'
    organisation_id = 'zhb'
    sets = '[erara, zhb, sosa, lara]'
    signature = 'zhb_'
    
### OAI configuration 

Wichtige Basisdaten fürs Harvesting, die in jedem Script angepasst werden müssen. Beispiel für e-rara:

    base_url = 'https://zenodo.org/oai2d'
    prefix = 'oai_dc'
    set_name = 'user-lara_e-rara'


### Export

Für jeden einzelnen record wird eine info.json-Datei erstellt im Format signature.json. Diese Dateien werden im directory 'info' abgelegt. 
Das ganze Set wird am Ende noch als json- und Excel-Datei exportiert.

### Marcxml aus Alma (SRU)

Mit der alma_id werden die MARC-Daten via SRU aus Alma extrahiert und abgespeichert unter signature.xml im directory 'metadata'.
SRU Doku: 
https://developers.exlibrisgroup.com/alma/integrations/sru/ 
https://slsp.atlassian.net/wiki/spaces/PSI/pages/77530997/SRU+Z39.50


### Datenobjekte abholen

Dies wird je nach Collection etwas unterschiedlich gehandhabt, da die Datenobjekte nicht einheitlich bezeichnet sind. Die Datenobjekte sollten grundsätzlich im directory 'objects' abgelegt sein.
