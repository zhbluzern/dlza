# Erstellung der gocfl create Befehle

Dieses Jupyiter Notebook erstellt die gocfl create-Befehle für eine bestimmte Collection. 
Die Doku für den Aufbau eines gocfl create Befehls befindet sich hier: https://github.com/je4/gocfl/blob/main/docs/create.md

### Caveat: manuelles entzippen

Die AIPs liegen nun als ZIP-File im Ordner Objects, im Unterordner der jeweiligen Signatur. Es macht keinen Sinn, ZIP-Files in ein ZIP-Archiv zu ingesten. Daher müssen die ZIP-Files vor dem Ingest entzippt und die Ordner danach bereinigt werden (ZIP-Files löschen). Dies sind zum Zeitpunkt alles manuelle Prozesse. 

Dieses Notebook geht davon aus, dass im Unterordner objects/{signature}/ ein weiterer Unterordner liegt, dessen Content ins Archiv gelagert wird. Ist dies nicht der Fall, wird das Script abgebrochen.  
    

## config.py

In der Config wird die aktuell zu verarbeitende Collection sowie diverse Dateipfade konfiguriert. Bspw. für E-Manuscripta:

    collection_id = 'sosa_emanus'
    dlza_root = 'd:/Ingest'
    gocfl_conf = 'd:/Ingest/config/zhb-config.toml'

## signature

Die Signature ist zentral für die Erstellung des storage roots, sowie das Auffinden der Objekt-Pfade, Metadaten und Info-Dateien. Grundsätzlich sollte für jede Collection eine Textdatei namens '/signatures.txt' mit den signatures vorliegen. Diese werden entweder durch ein anderes Jupyter Notebook konfiguriert oder können von Hand erstellt werden.
Der Dateipfad kann konfiguriert werden. 

## objects
Das script prüft nicht, ob die SIP-Objekte tatsächlich vorhanden bzw. entzippt sind, dies muss vorher (manuell) überprüft werden. 


## storage root

Hier wird davon ausgegangen, dass der storage root ein ZIP file sein soll. Für jede signature wird ein storage_root angelegt. 


##  Create Befehl für gocfl generieren

Die gocfl create Befehle für alle Signaturen werden gemäss https://github.com/je4/gocfl/blob/main/docs/create.md erstellt. Der Pfad für die Config.toml kann konfiguriert werden.  

Muster:

    gocfl create ./archiv.zip ./object-directory metadata:./metadata-directory --config ./config/gocfl.toml -i 'signature'  --ext-NNNN-metafile-source ./info.json
    
Das Script [create_gocfl.py](create_gocfl.py) erstellt für jedes Objekt eine Textdatei mit dem jeweiligen Create-Befehl. 

*TODO: direkt ein .ps erstellen für Workbench*

## Display Befehl für gocfl generieren

Das Notebook erstellt zusätzlich den Display-Befehl gemäss https://github.com/je4/gocfl/blob/main/docs/display.md .
Der Display-Befehl wird in eine neue Zeile in das dazugehörige Create-Textfile geschrieben. 

Ausserdem wird der Name für die Report-Datei ins File geschrieben, so dass er auf der Workbench leicht kopiert werden kann.  

## Zurück zur Übersicht

[Readme](Readme.md)