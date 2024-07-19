# 2 - Metadaten abholen

Für gocfl müssen die semantischen Metadaten pro Objekt in einem eigenen Ordner 'metadata' liegen. 

### Metadaten aus Alma (SRU, marcxml/MODS)

Mit der MMS ID werden die Metadaten via SRU als marcxml und MODS aus Alma extrahiert und abgespeichert unter collection/sip/metadata/mmsid.xml.

### Datacite - Dublin Core - ZenodoMARC (OAI, XML/json)

Daten aus Zenodo-Repositories werden mit Datacite-, Dublin-Core- und MARC-Metadaten ins Archiv eingelagert.
Dazu wird die Zenodo-ID und das OAI-Set benötigt.
Für Zenodo-Daten soll immer auch die komplette API-Response mitgespeichert werden, da nur hier die access-rights und allfälligen Embargo-Daten hinterlegt sind.
Rate Limiting Daten für Zenodo (OAI und API): <https://about.zenodo.org/principles/> Punkt 11

### TEI

E-codices Beschreibungen im TEI Format (XML). Http-request auf e-codices-Webseite.

### Weitere Metadaten

z.B. OCR/Aalto, etc. (TODO)

## Vorgehen

Aufruf des Python scripts [create_metadata.py](create_metadata.py) über Kommandozeile:

```
python create_metadata.py
```

## Nächstes Kapitel

[3 - Objekte anlegen](3_Objekte.md)

## Vorheriges Kapitel

[1 - Inventar erstellen](1_Inventar.md)
