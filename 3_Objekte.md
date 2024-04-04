# 3 - Datenobjekte abholen


Dieses Script erstellt in 'object' die Unterordner mit dem Identifier, die Files werden ohne weitere Zwischenverarbeitung oder Prüfung hierhin kopiert. 
Das Migrieren sowie Entzippen erfolgt vorerst manuell. 

## Variante A: Datenobjekte liegen auf einem Laufwerk

Gültig für Digitalisate aus der Sosa, bzw. Objekte, die auf lokalen Laufwerken liegen. 
Achtung! Dieses Python script kann in der Ausführung sehr lange dauern, da die Dateien riesig sind. 
Voraussetzung: mit VPN verbunden / im unilu-Netzwerk, mit Laufwerk G verbunden.

Aufgrund der geringen Menge und der diversen Metadatenquellen werden diese Zipkapseln von Hand vom Laufwerk G auf die Workbench verschoben. Sie werden alle manuell entzippt. 

Die Zipkapseln sind alle nach folgender Struktur oder ähnlich benannt:

    000190118_20150320T000256_master_ver1.zip
    10_7891_e-manuscripta-108732.zip

Die Objekte liegen auf G:\ZHB-Sosa_Digital\digital. Die vollständigen Pfade auf G sind in der Eingabedatei ergänzt und ist in die Infojson unter 'additional' abgelegt. 
Der Dateipfad auf der Workbench wird nach dem DOI benannt. 

Aufruf via Konsole:
```
python copy_zip_from_directory.py
```

## Variante B: Download aus Zenodo

Die Datenabholung für Zenodo-Repositories funktioniert etwas anders: mittels HTTP download direkt von zenodo. Script: [copy_zip_from_directory.py](copy_zip_from_directory.py)


Aufruf via Konsole:
```
python copy_zip_from_zenodo.py
```

### Delay (rate limiting)

Global limit for guest users: 60 requests per minute, 2000 requests per hour
OAI-PMH API harvesting: 120 requests per minute
=> pro loop 1 Sekunde sleep() einbauen. 

## Nächstes Kapitel 

[4 - GOCFL](4_gocfl.md)

## Vorheriges Kapitel


[2 - Metadaten](2_Metadaten.md)
