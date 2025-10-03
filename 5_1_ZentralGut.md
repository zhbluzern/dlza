# Dokumentation der Anbindung von ZentralGut an die DLZA

## Einleitung

Das Pythonskript `create_inventory_from_zentralgut.py` ist in der Lage folgende Schritte durchzuführen:
* Abfrage beliebiger Datensätze in ZentralGut über die GoobiWorkflow-Rest-API mit der Goobi-Workflow-Syntax
* Auf Basis der zurückgegebenen Datensätze wird ein Inventar angelegt, sowie einzelne Ordner je Objekt mit den Unterordner (data, metadata, ingest)
* Es werden verschiedene Metadaten abgefragt, zumindest jedoch die Goobi-Workflow meta.xml, das transformierte mets/mods.xml und wenn verfügbar ein ALMA-MARCXML im Original
* Das Skript kann vom ZentralGut-S3-Storage die nötigen Dateien laden (jedenfalls Master-Image und wenn vorhanden, OCR-ATLO.xml, OCR.txt, Original-Import, Seitensplit.pdf)

## Requirements

### Umgebung
Um mit der Goobi-Workflow-REST-API kommunizieren und vom S3-Storage Daten beziehen zu können, muss das Skript
* in der VPN-Range UniLu/ZHB ausgeführt werden.
* ein SSH-User mit Privatekey für GoobiWorkflow vorhanden sein und die Credentials in einem .env File hinterlegt werden
* S3-Storage-Credentials in .env hinterlegt weren.

### Python-Requirements
* Python-Library paramiko ist für das SSH-Handling zuständig: `pip install paramiko`
* Pyton-Library boto3 für den S3-Storage-Zugriff `pip install boto3`

## Inventar erzeugen

Das Inventar und die zugehörigen info.json Files werden auf Basis einer REST-API Anfrage an Goobi Workflow erzeugt. Es wäre auch eine Abfrage via OAI-PMH von ZentralGut möglich, es wird aber die Workflow-API-Anfrage aus folgenden Gründen bevorzugt:
* Ingest auch von Records für die DLZA die in Workflow zwar erfasst und gespeichert aber nicht für die Präsentation im Viewer gedacht sind (Metadatum `RestrictionOnAccess=NOACCESS`)
* Goobi-Workflow-Filter-Syntax erlaubt granulare Anfragen an den Datenbestand: 
  - Einzel-ID-Abfrage oder Abfrage ausgewählter Vorgänge mittels Goobi-Vorgangs-ID: `"ID:10946 10947 10945 10643 2623"` 
  - Metadaten-Spezifika (zB Singaturbereiche) 
  - Ausschluss von Records mit bereits bestehenden Wert (zB keine Records abfragen, die bereits in DLZA gelandet sind etc.)

Alternativ dazu ist auch der Bezug von ZentralGut-Records über OAI-PMH möglich:
```python
import src.oaiHandler as oaiHandler

for oaiSet in config.zentralgut_sets:
    print(f"{config.baseurl_zentralgut_oai}?verb=ListIdentifiers&metadataPrefix=oai_dc&set={oaiSet}")
    oaiHandler.harvestOai(config.baseurl_zentralgut_oai, {"verb":"ListRecords","metadataPrefix":"oai_dc","set":oaiSet},outputFileName=config.collection_id)
```

## Metadaten speichern
Es werden aus Goobi folgende Metadaten je Record für die DLZA gespeichert
* meta(_anchor).xml - Goobi-Workflow Metadaten-File
* mets.xml - Transformation in METS/MODS
* marc.xml - bei Vorliegen eines ALMA-Records als Metadatenbasis wird der ALMA-Datensatz parallel geharvestet und gespeichert.
* Zusätzlich wird noch die `ruleset.xml` gespeichert, die es ermöglichen würde, auf Basis des vorliegenden Archivs einen Ingest in eine neue Goobi-Workflow-Instanz einzuspielen, dadurch den Medateneditor valide zu halten und um eine unmittelbar valide Transformation in ein neues Viewer-System zu ermöglichen.
