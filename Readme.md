# Readme DLZA @ zhbluzern

Diese Jupyter Notebooks dienen zur Aufbereitung der Datenobjekte und Metadaten aus den Beständen der ZHB Luzern für die digitale Langzeitarchivierung (DLZA) der ZHB Luzern, basierend auf der GOCFL implementierung von Jürgen Enge, https://github.com/je4/gocfl .

Es werden Bestände der Sondersammlung (E-Rara, E-codices, etc.), aus dem Open-Science-Repositories (Lory, Lara) sowie weiteren Sammlungen aufbereitet. Für jede Sammlung (= collection) gibt es einen eigenen Workflow, aber folgender Basis-Workflow gilt für alle:


## Basiskonfiguration

Es wird eine info.json Datei nach folgendem Schema erstellt:
https://github.com/je4/gocfl/blob/main/gocfl-info-1.0.json 

Vereinfacht gesagt, muss eine info.json folgendermassen aussehen: 

    infoSet = {
        'additional': '',
        'address': config.address, 
        'collection': config.collection,
        'collection_id': config.collection_id,
        'created': now
        'identifiers': [],
        'ingest_workflow': config.ingest_workflow, 
        'last_changed': now
        'organisation' : config.organisation,
        'organisation_id' : config.organisation_id, 
        'references' : [],
        'sets' : config.sets,
        'signature': '', 
        'title' : '', 
        'user' : config.user       
    }

Pflichtfelder sind: "signature", "organisation_id", "organisation", "title", "user", "address", "created", "last_changed".

Die Signature ist die zentrale ID für die Erstellung der Archivkapseln und besteht daher aus einem dauerhaften Identifier (bspw. DOI). 

Im Config-File wird die Abteilung (bspw. zhb:...) hinzugefügt, das Script ergänzt den Identifier. 


### Config.py

Die config.py beinhaltet diverse Daten, welche nicht aus den bestehenden Metadaten (Schnittstelle) kommen, und kann pro Set konfiguriert werden (z.B. author, institution, etc.). Sie muss in einer bestimmten Struktur vorliegen (Details, siehe Notebook "Vorbereitung").
Die Config bilden sowohl Mandant, Datenproduzent und Collection ab. Das Feld 'additional' kann für alles Mögliche verwendet werden, wir notieren hier Dateinamen oder Dateipfade im Originalsystem. 
Die config.py beinhält auch die Schnittstellen-Konfigurationen (z.B. Metadatenformate, Basis-URL für OAI-PMH, etc.)


### Export

Für jeden einzelnen record wird eine info.json-Datei erstellt im Format signature.json. Diese Dateien werden im directory 'info' abgelegt. 
Das ganze Set wird am Ende noch als json- und Excel-Datei exportiert.


### Metadaten (Alma, weitere Systeme)

Mit der alma_id werden die MARC-Daten via SRU aus Alma extrahiert und abgespeichert unter signature.xml im directory 'metadata'.
Weitere Metadaten (z.B. METS/MODS-Daten) können aus andern Systemen hinzugefügt werden. 
Wichtig: die Metadaten müssen pro Objekt in einem eigenen directory zusammegefasst werden. 


### Datenobjekte abholen

Dies wird je nach Collection etwas unterschiedlich gehandhabt, da die Datenobjekte nicht einheitlich bezeichnet sind. Die Datenobjekte sollten grundsätzlich im directory 'objects' abgelegt sein.
