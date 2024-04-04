
# 1 - Erstellung der info.json und des Inventory

Ein Python-Script erstellt eine info.json Datei für alle Objekte der Collection und legt sie im Ordner 'info' als JSON Datei ab.
Doku der Info.json, siehe GOCFL-implementierung von Jürgen Enge, https://github.com/je4/gocfl . 
Vorlage: https://github.com/je4/gocfl/blob/main/gocfl-info-1.0.json 


## Export info.json

Für jeden einzelnen record wird eine info.json-Datei erstellt im Format info/{signature}.json.
Das ganze Set wird am Ende noch als json- und Excel-Datei exportiert ins working directory als Inventar, welche Datenobjekte eingelagert wurden. 

## Variante A: Input-File aus Excel (Alma) 

Standardverfahren: Viele collections der ZHB können mit einer Eingabedatei verarbeitet werden, die relativ leicht aus Alma exportiert werden kann. Die Sammlungen der Sosa sind alle in Alma in einem öffentlichen Set in der RZS gelistet. 

Die Export-Datei aus Alma wird leicht überarbeitet. Nicht benötigte Spalten werden gelöscht, einige Daten müssen gesplitted werden. Folgende Spalten werden benötigt:

- Title
- Record number: wird vorerst nicht benötigt, kann trotzdem stehengelassen werden (alte HAN-Nummer).
- Call number: aus Spalte Availability splitten, Spalte umbenennen 
- MMS_ID als Text erzwingen (Bsp. '9914249335105505')
- DOI manuell ergänzen
- Dateipfad manuell ergänzen
- externe ID wie z.B. E-Manuscripta ID, E-Codices-Identifier manuell ergänzen

Da die Sosa-Sammlungen der ZHB zur Zeit überschaubar sind, hält sich der zeitliche Aufwand dafür in Grenzen. 
Als Alternative zum Direkt-Export aus Alma könnte auch die Excel-App "Excel Alma Lookup" verwendet werden. 
Mehr dazu: https://github.com/pulibrary/ExcelAlmaLookup

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