# Erstellung der gocfl create Befehle

Dieses Python script erstellt die gocfl create-Befehle für eine bestimmte Collection.
Die Doku für den Aufbau eines gocfl create Befehls befindet sich hier: <https://github.com/je4/gocfl/blob/main/docs/create.md>

Dieses Script geht davon aus, dass im Unterordner objects/{signature}/ ein weiterer Unterordner liegt, dessen Content ins Archiv gelagert wird.

## config.py

In der Config wird die aktuell zu verarbeitende Collection sowie diverse Dateipfade konfiguriert. Bspw. für E-Manuscripta:

    collection_id = 'sosa_emanus'
    dlza_root = 'd:/Ingest'
    gocfl_conf = 'd:/Ingest/config/zhb-config.toml'

### signature

Die Signature ist zentral für die Erstellung des storage roots, sowie das Auffinden der Objekt-Pfade, Metadaten und Info-Dateien.  

### objects

Das script prüft nicht, ob die SIP-Objekte tatsächlich vorhanden bzw. entzippt sind, dies muss vorher (manuell) überprüft werden.

### storage root

Hier wird davon ausgegangen, dass der storage root ein ZIP file sein soll. Für jede signature wird ein storage_root angelegt.

## Create Befehl für gocfl generieren

Die gocfl create Befehle für alle Signaturen werden gemäss <https://github.com/je4/gocfl/blob/main/docs/create.md> erstellt. Der Pfad für die Config.toml kann konfiguriert werden.  

Muster:

    gocfl create ./archiv.zip ./object-directory metadata:./metadata-directory --config ./config/gocfl.toml -i 'signature'  --ext-NNNN-metafile-source ./info.json

Das Script [create_gocfl.py](create_gocfl.py) erstellt für jedes Objekt eine ausführbare Datei (.dat) mit dem jeweiligen Create-Befehl. Aufruf:

    python create_gocfl.py

## Display Befehl für gocfl generieren

Das Script erstellt zusätzlich den Display-Befehl gemäss <https://github.com/je4/gocfl/blob/main/docs/display.md> .
Der Display-Befehl wird in eine neue, ausführbare Datei (.dat) in das dazugehörige Display-File geschrieben.

## Weitere Schritte

Alle weiteren Arbeiten finden auf der DLZA-Workbench statt (GOCFL). Die genaue Doku dazu ist auf Stackfield (ZHB-Intern). Kurzfassung:

1. Gesamter collection-ordner auf Viren überprüfen
2. Je nach Objects: Dateien umwandeln in andere Formate (z.B. PDF/A)
3. Collection-Ordner auf Workbench verschieben (mittels Transfer-Laufwerk)
4. Auf Workbench: Wenn notwendig, Zipkapseln entzippen
5. Auf Workbench: Tika starten
6. Auf Workbench: gocfl-create-Datei ausführen, Konsole auf Fehlermeldungen prüfen
7. Auf Workbench: gocfl-display-Datei ausführen, Report erstellen
8. gocfl-Archivkapseln mittels ONA nach Basel schicken (TODO)
9. Reports und Inventory auf ZHB-DLZA ablegen. (TODO)
10. Update in Originalsysteme ausführen (TODO)

## Zurück zur Übersicht

[Readme](Readme.md)
