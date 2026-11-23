# Aufbau von event.json (schemaVersion 1)

| Feld | Inhalt |
|---|---|
| `schemaVersion` | immer `1` |
| `updatedAt` | Zeitstempel der letzten Änderung (ISO 8601) |
| `event.name`, `subtitle`, `edition` | Name, Unterzeile, Jahrgang |
| `event.timeZone` | `Europe/Berlin` |
| `event.days[]` | `date` (JJJJ-MM-TT), `label` (Freitag), `opens`, `closes` (HH:MM; `closes` vor `opens` = nach Mitternacht) |
| `event.venue` | `name`, `address`, optional `lat`, `lon`, `placeholder` |
| `event.ticketUrl` | Ticketshop (https) |
| `event.contactEmail`, `website`, `imprintUrl`, `privacyUrl` | Kontakt und Rechtliches |
| `event.social[]` | `type`, `label`, `url` |
| `notices[]` | `id`, `date`, `title`, `text`, `important` (hervorgehoben) |
| `artists[]` | `id`, `name`, `description`, optional `image` |
| `timetable.placeholder` | `true` = Zeiten vorläufig |
| `timetable.stages[]` | `id`, `name` |
| `timetable.slots[]` | `id`, `day` (Veranstaltungstag), `start`, `end`, `stage`, `artistId` oder `title`. Uhrzeiten vor 06:00 zählen zur Nacht nach `day`. |
| `abc[]` | `term`, `text` (Reihenfolge = Anzeige) |
| `map.plan` | `image` (relativ, optional; ohne Bild zeigt die App eine Skizze), `aspectRatio` (Breite/Höhe), `note`, `placeholder` |
| `map.pois[]` | `id`, `type` (eingang, buehne, bar, essen, wc, garderobe, erste_hilfe, parken, biergarten, info), `name`, `x`, `y` (0 bis 1 von links oben), `description` |
| `map.arrival` | `address`, `parkingText`, `publicTransportText`, optional `parkingLat`, `parkingLon`, `placeholder` |

Regeln (prüft `tools/pruefen.py` und die App): ids eindeutig, `artistId` und `stage` existieren, `day` ist ein Veranstaltungstag, Auftritte auf derselben Bühne überlappen nicht, Links beginnen mit https://.
