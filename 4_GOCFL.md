# Erstellung der gocfl create Befehle

Dieses Python script erstellt die gocfl create-Befehle für eine bestimmte Collection.
Die Doku für den Aufbau eines gocfl create Befehls befindet sich hier: <https://github.com/je4/gocfl/blob/main/docs/create.md>

Dieses Script geht davon aus, dass im Unterordner collection/sip/data das Objekt liegt, welches ins Archiv gelagert wird.

## config.py

In der Config wird die aktuell zu verarbeitende Collection sowie diverse Dateipfade konfiguriert, siehe [Readme](Readme.md)

### signature

Die Signature ist zentral für die Erstellung des storage roots, sowie das Auffinden der Objekt-Pfade, Metadaten und Info-Dateien.  

### data

Das script prüft nicht, ob die SIP-Objekte tatsächlich vorhanden bzw. entzippt sind, dies muss vorher (manuell) überprüft werden.

### storage root

Hier wird davon ausgegangen, dass der storage root ein ZIP file sein soll. Für jede signature wird ein storage_root angelegt.

## Create Befehl für gocfl generieren

Die gocfl create Befehle für alle Signaturen werden gemäss <https://github.com/je4/gocfl/blob/main/docs/create.md> erstellt. Der Pfad für die Config.toml kann konfiguriert werden.  

Muster:

    gocfl create ./archive.zip ./data-directory metadata:./metadata-directory --config ./config/gocfl.toml -i 'signature'  --ext-NNNN-metafile-source ./ingest/info.json

Das Script [create_gocfl.py](create_gocfl.py) erstellt für jedes Objekt eine ausführbare Datei (.ps1) mit dem jeweiligen Create-Befehl. Aufruf:

    python create_gocfl.py

## Display Befehl für gocfl generieren

Das Script erstellt zusätzlich den Display-Befehl gemäss <https://github.com/je4/gocfl/blob/main/docs/display.md>.
Der Display-Befehl wird in eine neue, ausführbare Datei (.ps1) in das dazugehörige Display-File geschrieben.

## ONA Befehl generieren

Das Script erstellt zusätzlich zwei .ps1-Dateien mit den ona-Befehlen, siehe https://gitlab.switch.ch/ub-unibas/dlza/ona sowie interne Doku auf Stackfield. 

## Weitere Schritte

Alle weiteren Arbeiten finden auf der DLZA-Workbench statt (GOCFL). Die genaue Doku dazu ist auf Stackfield (ZHB-Intern). Kurzfassung:

1. Gesamter collection-ordner auf Viren überprüfen
2. Je nach SIP: Dateien analysieren mit DROID und bei Bedarf vorher in Archiv-Format umwandeln.
3. Collection-Ordner auf Workbench verschieben (mittels Transfer-Laufwerk)
4. Auf Workbench: Wenn notwendig, Zipkapseln entzippen, Metadaten aus ZIP-Kapseln von data zu metadata directory verschieben
5. Auf Workbench: Tika starten
6. Auf Workbench: gocfl-create-Datei ausführen, Konsole auf Fehlermeldungen prüfen
7. Auf Workbench: gocfl-display-Datei ausführen, Report erstellen
8. gocfl-Archivkapseln mittels ONA nach Basel schicken
9. DLZA-Monitoring prüfen (sind AIP auf den storages angekommen und korrekt?)
10. Inventory/Reports auf ZHB-DLZA ablegen, Workbench aufräumen.
11. Update in Originalsysteme ausführen (TODO)

## Zurück zur Übersicht

[Readme](Readme.md)
