
# 1 - Erstellung der info.json und des Inventory

Ein Python-Script erstellt eine info.json Datei für alle Objekte der Collection und legt sie im Ordner 'ingest' als JSON Datei ab.
Doku der info.json, siehe GOCFL-implementierung von Jürgen Enge, <https://github.com/je4/gocfl> .
Vorlage: <https://github.com/je4/gocfl/blob/main/gocfl-info-1.0.json>

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

## Export info.json

Für jeden einzelnen record wird eine info.json-Datei erstellt im Ingest-Ordner. 
Das ganze Set wird am Ende noch als json- und Excel-Datei exportiert ins working directory als Inventar, welche Datenobjekte eingelagert wurden.

## Variante A: Input-File aus Excel (Alma)

Standardverfahren (für ZHB-Bestände): 
Viele collections können mit einer Eingabedatei verarbeitet werden, die relativ leicht aus Alma exportiert werden kann. Die Sammlungen der ZHB sind alle in Alma in einem öffentlichen Set in der RZS gelistet. Eine separate Anleitung dazu findet sich auf Stackfield, Schulungsunterlagen zur Erstellung von Sets gibt es bei SLSP oder Ex Libris. 

Die Export-Datei aus Alma wird leicht überarbeitet. Nicht benötigte Spalten werden gelöscht, einige Daten müssen gesplitted werden. Folgende Spalten werden benötigt (Reihenfolge der Spalten ist irrelevant):

- Type / Creator / Imprint: Spalte umbenennen zu "Description"
- Title: unverändert übernehmen (Titel)
- Record number: unverändert übernehmen (alte HAN-Nummer)
- Availabilty: Spalte splitten, es wird nur die Signatur benötigt. Spalte umbenennen zu 'Call number'
- MMS ID: als Text erzwingen (Bsp. '9914249335105505') (Python script [get_network_id_from_alma.py](get_network_id_from_alma.py) übernimmt dies auch.)
- DOI: manuell ergänzen (alternativ: mit Excel Alma Lookup tool aus MARC-Feld 024$a)
- Dateipfad: manuell ergänzen (Angaben von Sosa erfragen)
- externe ID: wie z.B. E-Manuscripta ID, E-Codices-Identifier manuell ergänzen
- License Data: manuell ergänzen. Für Sosa-Bestände normalerweise PDM 1.0 Deed (Public Domain).
- License Metadata: manuell ergänzen. Für Sosa-Bestände normalerweise CC0 oder CC BY.
- Network ID: Spalte manuell oder mit separatem Python script [get_network_id_from_alma.py](get_network_id_from_alma.py) ergänzen. Das ist die Alma NZ ID (aus MARC-Feld 35a, z.B. '(EXLNZ-41SLSP_NETWORK)991134908649705501').

Da die Sosa-Sammlungen der ZHB zur Zeit überschaubar sind, hält sich der zeitliche Aufwand dafür in Grenzen.
Als Alternative zum Direkt-Export aus Alma könnte auch die Excel-App "Excel Alma Lookup" verwendet werden.
Mehr dazu: <https://github.com/pulibrary/ExcelAlmaLookup>

Die Eingabedatei wird so benannt, wie im Config-File vorgegeben und muss im working directory liegen.
Nun kann das folgende Script ausgeführt werden: [create_inventory_from_xlsx-alma.py](create_inventory_from_xlsx-alma.py). Es liest die Daten aus der Eingabedatei und erstellt für jeden record die info.json.

Aufruf via Kommandozeile im Root-Verzeichnis:

```
python create_inventory_from_xlsx-alma.py
```

## Variante B, Teil 1: Input-File aus Zenodo

Standardverfahren für alle Zenodo-Repository-Daten (Lory, Lara):
Diese collections der ZHB können ebenfalls mit einer Eingabedatei verarbeitet werden.  Sie kann mit dem folgenden Script aus Zenodo exportiert werden: [create_excel_from_zenodo.py](create_excel_from_zenodo.py). Danach liegt eine Excel-Datei im working directory.
Der Name der Datei sowie die Zenodo-Community werden in der config.py angegeben.

*Wichtig: community_id in config.py muss wie die Zenodo-ID lauten, damit das Skript funktioniert.*

Aufruf:

```
python create_excel_from_zenodo.py
```

## Variante B, Teil 2: Info.json aus Zenodo

Nun wird die Infojson erstellt, ähnlich wie in Variante A, mit folgendem Script: [create_inventory_from_xlsx-zenodo.py](create_inventory_from_xlsx-zenodo.py)

Aufruf:

```
python create_inventory_from_xlsx-zenodo.py
```

## Nächstes Kapitel

[2 - Metadaten](2_Metadaten.md)

## Vorheriges Kapitel

[Readme](Readme.md)
