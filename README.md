# Inhalte der Eschweiler-Wiesn-App

Die App lädt `content/v1/event.json` von
`https://raw.githubusercontent.com/Jumpmaster2/wiesn-event-app-inhalte/main/content/v1/event.json`
und speichert sie auf dem Gerät. Änderungen hier erscheinen ohne App-Update (GitHub-Cache: wenige Minuten).

## Ändern
1. `content/v1/event.json` bearbeiten (Aufbau: siehe `SCHEMA.md`).
2. Prüfen: `python3 tools/pruefen.py` muss `gueltig` melden.
3. Committen und pushen.

Bilder (z. B. der Geländeplan) liegen unter `content/v1/img/` und werden relativ angegeben, z. B. `"image": "img/gelaende.png"`.
Felder mit `"placeholder": true` zeigt die App als „Vorläufig“ an.

Wird das Format inkompatibel geändert, kommt es nach `content/v2/` und `schemaVersion` steigt; ältere Apps behalten dann ihre letzte Kopie und bitten um ein Update.
