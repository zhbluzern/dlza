# Readme DLZA @ zhbluzern

Diese Python scripts dienen zur Aufbereitung der SIP (Datenobjekte und Metadaten) aus den Beständen der ZHB Luzern für die digitale Langzeitarchivierung (DLZA), basierend auf der GOCFL implementierung von Jürgen Enge, <https://github.com/je4/gocfl> .

Es werden Bestände der Sondersammlung (E-Rara, E-codices, etc.), aus dem Open-Science-Repositories (LORY, LARA) sowie Sammlungen aus Zentralgut aufbereitet. Für jede Sammlung (= collection) gibt es einen eigenen Workflow (internes Dokument auf Stackfield), aber folgender Basis-Workflow gilt für alle Sammlungen.

## Voraussetzungen

Damit die Python scripts funktionieren, müssen folgende Voraussetzungen erfüllt sein:

### Technische Vorbereitungen

Alle Scripts müssen lokal auf dem Rechner laufen. Dazu muss Python installiert sein. Die Scripts werden in das lokale Verzeichnis kopiert, welches in der config.py als user_root angegeben wird (siehe nächster Punkt).

Python-Bibliotheken nachinstallieren: z.b. mittels

    pip install python-dotenv

Sämtliche SIP werden lokal erstellt, bzw. vorbereitet. Erst danach (und nach Virencheck) werden die fertigen SIP auf die DLZA Workbench geschoben.
Die DLZA Workbench der ZHB (Windows-Server) kommt nur für GOCFL und ONA (Verschiebung der AIP nach Basel) zum Einsatz. Diese Prozesse sowie die Konfiguration der Workbench sind in einem internen Dokument beschrieben (Stackfield).

### Eingabedateien

Für alle weiteren Schritte wird eine Eingabedatei (xlsx) benötigt mit den Titeln dieser Collection. Es wird im [Kapitel 1](1_Inventar.md) näher erläutert, wie die Datei aufbereitet sein soll.
Die Eingabedateien werden nicht auf Github veröffentlicht.

### API Keys im .env file

Nicht veröffentlicht auf Github.  
Für access_token, API keys, etc. braucht es ein .env file im root directory. Die entsprechenden API-Keys für Alma können auf developers.exlibrisgroup.com erstellt werden, die tokens für Zenodo auf zenodo.org.
Siehe [Using env files for environment variables in python applications](https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1)

## Basiskonfiguration mit config.py

Auf Github wird nur eine Beispieldatei der config.py veröffentlicht. Die ZHB-Spezifikationen für die config.py sind in einem internen Dokument (Stackfield) festgehalten.
Bei jedem Workflow bzw. für jede Collection ist das Anpassen der Datei config.py notwendig.
Die Datei kann mit einem Editor (z.B. notepad++ oder VS Code) geöffnet und bearbeitet werden, wie eine normale Textdatei. Die config.py muss ebenfalls im lokalen Verzeichnis liegen (gleiche Ebene wie scripts und .env file).

Die config.py beinhaltet diverse Daten, welche nicht aus den bestehenden Metadaten (Schnittstelle) kommen, und kann pro Collection konfiguriert werden (z.B. author, institution, etc.). Sie muss in einer bestimmten Struktur vorliegen (Details unten).
Die Config bilden sowohl Mandant, Datenproduzent und Collection ab. Das Feld 'additional' kann für alles Mögliche verwendet werden, wir notieren hier Dateinamen oder Dateipfade im Originalsystem.
Die config.py beinhält auch die Schnittstellen-Konfigurationen (z.B. Metadatenformate, Basis-URL für OAI-PMH, etc.). Die config-Datei sollte nach Abschluss der Ingest-Vorbereitungen mit dem Collection-Inventory weggespeichert werden.

Die Konfigurationen, welche für jeden Ingest angepasst werden müssen, sind markiert.

*not allowed: characters ~ “ # % & * : < > ? / \ { | }*

### collection (anpassen)

Dieser Bereich muss für jede collection angepasst werden. Bsp. E-Manuscripta:

    collection_id = 'emanus'
    collection = 'ZHB Sosa E-Manuscripta'
    zenodo_set = 'user-zenodocommunity' # Zenodo OAI set name, eg. user-lory
    ingest_workflow = 'e-manuscripta'
    keywords = []  # array
    sets = ['e-manuscripta', 'zhb']
    input_file = 'e-manuscripta.xlsx'


Aus diesem Abschnitt werden zentrale Daten für alle weiteren Schritte geholt. Die Bezeichnung des ingest-workflows wird auch für die URN benutzt.

### metadata formats (anpassen)

Hier wird angegeben, welche Metadaten für diese collection abgeholt werden, und über welche Schnittstelle.
Entsprechende Formate auf 'True' setzen, z.B. wenn MARC-Daten hinzugefügt werden sollen:

    marcxml = 'True'
    mets = 'False'
    mods = 'False'
    datacite = 'False'
    dc = 'False'
    apidata = 'False'
    tei = 'False'

Zu jedem Format sollte die Base-URL für die Abholung der Metadaten überprüft werden, z.B. Alma-SRU-Schnittstelle (IZ-spezifische Codes in der URL anpassen)

    marcxml_baseurl = 'https://slsp-rzs.alma.exlibrisgroup.com/view/sru/41SLSP_RZS?version=1.2&operation=searchRetrieve&recordSchema=marcxml&query=rec.id='

Nicht benötigte Metadatenformate auf 'False' setzen. Base-URL muss nur angepasst werden, wenn das Format auf true gesetzt ist.
Es sind noch nicht alle Metadatenformate abgedeckt (im Aufbau). Folgende Metadaten sind derzeit implementiert:

    marcxml (xml via SRU aus Alma)
    datacite/dc (xml via OAI aus Zenodo)
    api-data (json via http request von Zenodo REST API)
    tei (xml via http request von ecodices)

### user / organisation information

Name der Ingest-Person bzw. Ingest-Organisation sollte hier angepasst werden. Wichtig ist auch der Root-Ordner des users, in welchem die Daten aufbereitet werden, bevor sie zur Workbench verschoben werden. Muss i.d.R. nur einmal angepasst werden.

    user_name = 'Vorname Name'
    user_address = 'mailto:vorname.name@myinstitution.ch'
    user_root = "C:/temp"

    organisation = 'Zentral- und Hochschulbibliothek Luzern'
    organisation_id = 'zhb'
    organisation_address = 'mailto:organisation@myinstitution.ch'

### DLZA Workbench information

Wenn mit GOCFL weitergearbeitet wird, sollen hier die Pfade für den Ingest-Ordner sowie der Pfad für die gocfl-config konfiguriert werden, damit der Create-Befehl korrekt erstellt wird. Die angegebenen Pfade sind Beispiele, die ZHB-Workbench-Config findet sich auf Stackfield.

    dlza_root = 'C:/Ingest'
    gocfl_conf = 'config.toml'
    gocfl = 'gocfl.exe'
    ona_conf = 'ona-config.yml'

### general configuration

Basis-Url-Konfiguration für diverse Schnittstellen und Resolver. Hier muss normalerweise nichts angepasst werden (PrimoVE Permalink anpassen an eigene Institution).

    baseurl_doi = 'https://doi.org/'
    baseurl_alma = 'https://rzs.swisscovery.slsp.ch/permalink/41SLSP_RZS/ldslj8/alma'



## Workflow ZHB-DLZA (Kurzversion)

Die einzelnen Schritte werden ausführlich in den folgenden Kapiteln  beschrieben:

1. [Inventar](1_Inventar.md)
2. [Metadaten](2_Metadaten.md)
3. [Objekte](3_Objekte.md)
4. [GOCFL](4_GOCFL.md)

### Inventar

Für jede Archivkapsel der Collection wird eine info.json Datei nach folgendem Schema erstellt:
<https://github.com/je4/gocfl/blob/main/gocfl-info-1.0.json>

Für jeden einzelnen record wird eine info.json-Datei erstellt.
Zugleich wird die Ordnerstruktur 'collection/sip/' erstellt, darin jeweils die sub-directories 'metadata', 'data' und 'ingest'. Die info.json wird im ingest-directory abgelegt.
Das ganze Set wird am Ende noch als json- und Excel-Datei exportiert.

### Metadaten (Alma, Zenodo, weitere Systeme)

Mit der record id werden die MARC-/DC-Daten via SRU/OAI aus den Master-Systemen extrahiert und abgespeichert unter 'recid'.xml im directory 'metadata'.
Weitere Metadaten (z.B. METS/MODS-Daten) können aus andern Systemen hinzugefügt werden.
Wichtig: die Metadaten müssen pro SIP in einem eigenen directory 'metadata' zusammegefasst werden.

### Datenobjekte abholen

Dies wird je nach Collection etwas unterschiedlich gehandhabt, da die Datenobjekte nicht einheitlich bezeichnet sind. Die Datenobjekte sollten grundsätzlich im directory 'data' abgelegt sein. Für Zenodo gibt es ein Download-Script, für einige Digitalisierungsprojekte ein Kopier-Script, wenn die Originalsystempfade bekannt sind.

### GOCF-Befehle

Die gocfl-Befehle für 'create', 'display' und 'ona' werden mittels Script vorbereitet und als Batch-Dateien im ingest-directory abgelegt. Mehr dazu auf <https://github.com/je4/gocfl>

## Nächstes Kapitel

1. [Inventar](1_Inventar.md)
