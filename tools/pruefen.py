#!/usr/bin/env python3
"""Prueft content/v1/event.json mit denselben Regeln wie die App (ContentValidator.kt).
Aufruf: python3 tools/pruefen.py [pfad]  -> Exitcode 0 = gueltig."""
import json, sys, re
from datetime import date, time, datetime, timedelta

POI_TYPES = {"eingang", "buehne", "bar", "essen", "wc", "garderobe", "erste_hilfe", "parken", "biergarten", "info"}

def parse_time(v):
    if not isinstance(v, str) or not re.fullmatch(r"\d{2}:\d{2}", v): return None
    try: return time.fromisoformat(v)
    except ValueError: return None

def parse_date(v):
    try: return date.fromisoformat(v)
    except (TypeError, ValueError): return None

def at(day, t):
    d = day + timedelta(days=1) if t.hour < 6 else day
    return datetime.combine(d, t)

def check(c):
    err = []
    if c.get("schemaVersion") != 1: err.append("schemaVersion muss 1 sein")
    for k in ("updatedAt", "event"):
        if k not in c: err.append(f"{k} fehlt")
    e = c.get("event", {})
    for k in ("name", "days", "venue", "ticketUrl"):
        if not e.get(k): err.append(f"event.{k} fehlt")
    for d in e.get("days", []):
        if not parse_date(d.get("date")): err.append(f"event.days: Datum {d.get('date')} ungueltig")
        for k in ("opens", "closes"):
            if not parse_time(d.get(k)): err.append(f"event.days {d.get('date')}: {k} ungueltig")
    links = [e.get("ticketUrl", "")] + [s.get("url", "") for s in e.get("social", [])] + \
            [e.get(k) for k in ("website", "imprintUrl", "privacyUrl") if e.get(k)]
    err += [f"Link {l} muss mit https:// beginnen" for l in links if not str(l).startswith("https://")]

    def ids(kind, items):
        seen = set()
        for i in items:
            if i.get("id") in seen: err.append(f"{kind}: id {i.get('id')} doppelt")
            seen.add(i.get("id"))
        return seen
    tt = c.get("timetable", {})
    ids("notices", c.get("notices", []))
    artists = ids("artists", c.get("artists", []))
    stages = ids("stages", tt.get("stages", []))
    ids("slots", tt.get("slots", []))
    ids("pois", c.get("map", {}).get("pois", []))
    days = {d.get("date") for d in e.get("days", [])}
    timed = []
    for s in tt.get("slots", []):
        sid = s.get("id")
        if not s.get("artistId") and not s.get("title"): err.append(f"slot {sid}: artistId oder title noetig")
        if s.get("artistId") and s["artistId"] not in artists: err.append(f"slot {sid}: artistId {s['artistId']} unbekannt")
        if s.get("stage") not in stages: err.append(f"slot {sid}: stage {s.get('stage')} unbekannt")
        if s.get("day") not in days: err.append(f"slot {sid}: day {s.get('day')} ist kein Veranstaltungstag")
        d, a, b = parse_date(s.get("day")), parse_time(s.get("start")), parse_time(s.get("end"))
        if not (d and a and b): err.append(f"slot {sid}: Zeit ungueltig"); continue
        start, end = at(d, a), at(d, b)
        if end <= start: end = datetime.combine(d + timedelta(days=1), b)
        timed.append((s.get("stage"), start, end, sid))
    timed.sort(key=lambda x: (x[0], x[1]))
    for x, y in zip(timed, timed[1:]):
        if x[0] == y[0] and y[1] < x[2]: err.append(f"Buehne {x[0]}: {x[3]} und {y[3]} ueberlappen")
    for p in c.get("map", {}).get("pois", []):
        if p.get("type") not in POI_TYPES: err.append(f"poi {p.get('id')}: Typ {p.get('type')} unbekannt")
        if not (0 <= p.get("x", -1) <= 1 and 0 <= p.get("y", -1) <= 1): err.append(f"poi {p.get('id')}: x/y muessen zwischen 0 und 1 liegen")
    return err

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "content/v1/event.json"
    with open(path, encoding="utf-8") as f: content = json.load(f)
    errors = check(content)
    for x in errors: print("FEHLER:", x)
    print("gueltig" if not errors else f"{len(errors)} Fehler")
    sys.exit(1 if errors else 0)
