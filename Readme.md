# Readme DLZA @ zhbluzern

Diese Python scripts dienen zur Aufbereitung der Datenobjekte und Metadaten aus den Beständen der ZHB Luzern für die digitale Langzeitarchivierung (DLZA) der ZHB Luzern, basierend auf der GOCFL implementierung von Jürgen Enge, <https://github.com/je4/gocfl> .

Es werden Bestände der Sondersammlung (E-Rara, E-codices, etc.), aus dem Open-Science-Repositories (LORY, LARA) sowie weiteren Sammlungen aufbereitet. Für jede Sammlung (= collection) gibt es einen eigenen Workflow, aber folgender Basis-Workflow gilt für alle Sammlungen.

## Voraussetzungen

Damit die Python scripts funktionieren, müssen folgende Voraussetzungen erfüllt sein:

### Technische Vorbereitungen

Alle Scripts müssen lokal auf dem Rechner laufen. Dazu muss Python installiert sein. Die Scripts werden in das lokale Verzeichnis kopiert, welches in der config.py als user_root angegeben wird (siehe nächster Punkt).

Python-Bibliotheken nachinstallieren: z.b. mittels

    !pip install python-dotenv

Sämtliche Metadaten und Objekte werden lokal erstellt, bzw. vorbereitet.
Erst danach (und nach Virencheck) werden die fertigen files auf die DLZA Workbench geschoben.

### Eingabedateien

Für alle weiteren Schritte wird ein Input file benötigt mit den Titeln dieser Collection. Es wird im [Kapitel 1](1_Inventar.md) näher erläutert, wie die Datei aufbereitet sein soll.

### API Keys im .env file

Nicht veröffentlicht auf Github.  
Für access_token, API keys, etc. braucht es ein .env file im root directory. Die entsprechenden API-Keys für Alma können auf developers.exlibrisgroup.com erstellt werden, die tokens für Zenodo auf zenodo.org.
Siehe [Using env files for environment variables in python applications](https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1)

## Basiskonfiguration mit config.py

Bei jedem Workflow bzw. für jede Collection ist das Anpassen der Datei config.py notwendig.
Die Datei kann mit einem Editor (z.B. notepad++ oder VS Code) geöffnet und bearbeitet werden, wie eine normale Textdatei. Die config.py muss ebenfalls im lokalen Verzeichnis liegen (gleiche Ebene wie scripts und .env file).

Die config.py beinhaltet diverse Daten, welche nicht aus den bestehenden Metadaten (Schnittstelle) kommen, und kann pro Collection konfiguriert werden (z.B. author, institution, etc.). Sie muss in einer bestimmten Struktur vorliegen (Details unten).
Die Config bilden sowohl Mandant, Datenproduzent und Collection ab. Das Feld 'additional' kann für alles Mögliche verwendet werden, wir notieren hier Dateinamen oder Dateipfade im Originalsystem.
Die config.py beinhält auch die Schnittstellen-Konfigurationen (z.B. Metadatenformate, Basis-URL für OAI-PMH, etc.). Die config-Datei sollte nach Abschluss der Ingest-Vorbereitungen mit dem Collection-Inventory weggespeichert werden.

Die Konfigurationen, welche für jeden Ingest angepasst werden müssen, sind markiert.

*not allowed: characters ~ “ # % & * : < > ? / \ { | }*

### collection (anpassen)

Dieser Bereich muss für jede collection angepasst werden. Bsp. E-Manuscripta:

    collection_id = 'sosa_e-manus'
    collection = 'ZHB Sosa E-Manuscripta'
    ingest_workflow = 'e-manuscripta'
    keywords = []  # array
    sets = ['e-manuscripta', 'zhb', 'sosa', 'lara']
    input_file = 'e-codices.xlsx'
    inventory_file = 'e-codices_inventory.json'
    inventory_xlsx = 'e-codices_inventory.xlsx'

Aus diesem Abschnitt werden zentrale Daten für alle weiteren Schritte geholt. Die Bezeichnung des ingest-workflows wird auch für die URN benutzt.

### metadata formats (anpassen)

Hier wird angegeben, welche Metadaten für diese collection abgeholt werden, und über welche Schnittstelle.
Entsprechende Formate auf 'True' setzen, z.B. wenn Dublin-Core-Daten hinzugefügt werden sollen:

    marcxml = 'False'
    datacite = 'True'
    dc = 'True'
    apidata = 'True'
    tei = 'False'

Zu jedem Format sollte die Base-URL für die Abholung der Metadaten überprüft werden, z.B. Alma-SRU-Schnittstelle:

    marcxml_baseurl = 'https://slsp-rzs.alma.exlibrisgroup.com/view/sru/41SLSP_RZS?version=1.2&operation=searchRetrieve&recordSchema=marcxml&query=rec.id='

Nicht benötigte Metadatenformate auf 'False' setzen. Base-URL muss nur angepasst werden, wenn das Format auf true gesetzt ist.
Es sind noch nicht alle Metadatenformate abgedeckt (im Aufbau). Folgende Metadaten sind derzeit implementiert:

    marcxml (xml via SRU aus Alma)
    datacite/dc (xml via OAI aus Zenodo)
    api-data (json via http request von Zenodo)
    tei (xml via http request von ecodices)

### user / organisation information

Name der Ingest-Person bzw. Ingest-Organisation sollte hier angepasst werden. Wichtig ist auch der Root-Ordner des users, in welchem die Daten aufbereitet werden, bevor sie zur Workbench verschoben werden. Muss i.d.R. nur einmal angepasst werden.

    user_name = 'Vorname Name'
    user_address = 'mailto:vorname.name@zhbluzern.ch'
    user_root = "G:/Research10/ZHB-DLZA/dlza_ingest"

    organisation = 'Zentral- und Hochschulbibliothek Luzern'
    organisation_id = 'zhb'
    organisation_address = 'mailto:lit@zhbluzern.ch'

### DLZA Workbench information

Hier muss in der Regel nichts angepasst werden. Die Pfade sind derzeit für die ZHB-Workbench konfiguriert.

    dlza_root = 'D:/Ingest'
    gocfl_conf = 'D:/Ingest/config/zhb-config.toml'
    gocfl = 'gocfl.exe'

### general configuration

Basis-Url-Konfiguration für diverse Schnittstellen und Resolver. Hier muss normalerweise nichts angepasst werden.

    baseurl_doi = 'https://doi.org/'
    baseurl_alma = 'https://rzs.swisscovery.slsp.ch/permalink/41SLSP_RZS/ldslj8/alma'

### subdirectories and file formats

Benötigte Ordnerstruktur. Hier sollte in der Regel nichts angepasst werden.
Diese Ordner müssen auch im lokalen Verzeichnis vorhanden sein:

Ordner mit name = collection_id, darin folgende Unterordner:

     info
     metadata
     objects      
     gocfl

Die weiteren Scripts basieren auf dieser Directory-Logik. Das Python script [create_dirs.py](create_dirs.py) kann dazu verwendet werden, diese Ordner automatisch aus der config.py zu erstellen. Dabei werden alle noch fehlenden Ordner erstellt, es wird nichts gelöscht oder überschrieben. Die Ordner können aber auch von Hand erstellt werden.

Aufruf des scripts in der Kommandozeile im Root-Ordner (z.B. mittels Shift-Rechtsklick, Powershell-Fenster hier öffnen):

```
python create_dirs.py
```

## Workflow ZHB-DLZA (Kurzversion)

Die einzelnen Schritte werden ausführlich in den folgenden Kapiteln  beschrieben:

1. [Inventar](1_Inventar.md)
2. [Metadaten](2_Metadaten.md)
3. [Objekte](3_Objekte.md)
4. [GOCFL](4_GOCFL.md)

### Inventar

Für jede Archivkapsel der Collection wird eine info.json Datei nach folgendem Schema erstellt:
<https://github.com/je4/gocfl/blob/main/gocfl-info-1.0.json>

Für jeden einzelnen record wird eine info.json-Datei erstellt mit Bezeichnung 'signature'.json. Diese Dateien werden im directory 'info' abgelegt. Das ganze Set wird am Ende noch als json- und Excel-Datei exportiert.

### Metadaten (Alma, Zenodo, weitere Systeme)

Mit der record id werden die MARC-/DC-Daten via SRU/OAI aus den Master-Systemen extrahiert und abgespeichert unter 'recid'.xml im directory 'metadata'.
Weitere Metadaten (z.B. METS/MODS-Daten) können aus andern Systemen hinzugefügt werden.
Wichtig: die Metadaten müssen pro Objekt in einem eigenen directory 'metadata' zusammegefasst werden.

### Datenobjekte abholen

Dies wird je nach Collection etwas unterschiedlich gehandhabt, da die Datenobjekte nicht einheitlich bezeichnet sind. Die Datenobjekte sollten grundsätzlich im directory 'objects' abgelegt sein. Für Zenodo gibt es ein Download-Script, für einige Digitalisierungsprojekte ein Kopier-Script, wenn die Originalsystempfade bekannt sind.

### GOCF-Befehle

Die gocfl-CREATE und DISPLAY Befehle werden mittels Script vorbereitet. Mehr dazu auf <https://github.com/je4/gocfl/blob/main/docs/create.md>

## Nächstes Kapitel

1. [Inventar](1_Inventar.md)
