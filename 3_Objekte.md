# 3 - Datenobjekte abholen

Dieses Script erstellt in 'data' die Unterordner mit dem Identifier, die Files werden ohne weitere Zwischenverarbeitung oder Prüfung hierhin kopiert.
Das Migrieren sowie Entzippen erfolgt vorerst manuell.

## Variante A: Datenobjekte liegen auf einem Laufwerk

Gültig für Digitalisate aus der Sosa der ZHB, bzw. im eingeschränkten Umfang für alle Objekte, die auf lokalen Laufwerken liegen.

*Achtung! Dieses Python script kann in der Ausführung sehr lange dauern, da die Sosa-ZIP-Kapseln riesig sind.
Das Skript hat daher einen Debug-Modus, bitte Anzahl der Objekte einstellen, die abgeholt werden sollen: Variable debug*

Voraussetzung an der ZHB: mit VPN verbunden / im UNET-Netzwerk, mit entsprechendem Laufwerk verbunden.

Die Zipkapseln liegen auf dem ZHB-Netzlaufwerk. Die vollständigen Pfade auf G sind in der Eingabedatei ergänzt und ist in der info.json unter 'additional' abgelegt.
Der Dateipfad auf der Workbench wird nach dem DOI benannt. Script: [copy_zip_from_directory.py](copy_zip_from_directory.py)
Aufgrund der geringen Menge und der diversen Metadatenquellen werden diese Zipkapseln von Hand auf die Workbench verschoben. Sie werden zur Zeit auch alle manuell entzippt.

Aufruf via Konsole:

```
python copy_zip_from_directory.py
```

## Variante B: Download aus Zenodo

Die Datenabholung für Zenodo-Repositories funktioniert etwas anders: mittels HTTP download direkt von zenodo.

*Achtung! Dieses Python script kann in der Ausführung sehr lange dauern, da die Dateien teilweise riesig sind.
Skript hat daher einen Debug-Modus, bitte Anzahl der Objekte einstellen, die abgeholt werden sollen: Variable debug*

Script: [copy_zip_from_zenodo.py](copy_zip_from_zenodo.py)

Aufruf via Konsole:

```
python copy_zip_from_zenodo.py
```

### Delay (rate limiting)

Global limit for guest users: 60 requests per minute, 2000 requests per hour
OAI-PMH API harvesting: 120 requests per minute
=> pro loop 1 Sekunde sleep() einbauen.

### TODO: manuelles entzippen

Die AIPs liegen nun in einigen Fällen als ZIP-File im Ordner 'objects', im Unterordner der jeweiligen Signatur. Es macht keinen Sinn, ZIP-Files in ein ZIP-Archiv zu ingesten. Daher müssen die ZIP-Files vor dem Ingest entzippt und die Ordner danach bereinigt werden (ZIP-Files löschen). Dies sind zum aktuellen Zeitpunkt alles manuelle Prozesse. Das Entzippen kann auch erst auf der Workbench stattfinden, so dauert der Transfer nicht so lange.

## Nächstes Kapitel

[4 - GOCFL](4_GOCFL.md)

## Vorheriges Kapitel

[2 - Metadaten](2_Metadaten.md)
