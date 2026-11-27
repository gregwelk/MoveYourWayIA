"""Keep the tracker map's county totals up to date.

data/pledge-log.csv    one line per pledge: date,county (no names, emails or pledge text)
data/pledge-counts.csv the 99 county totals the map reads, rebuilt from the log every run

Usage: update_pledge_counts.py [--add "County name"] [--date YYYY-MM-DD]
"""
import argparse
import csv
import datetime
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG = os.path.join(ROOT, "data", "pledge-log.csv")
COUNTS = os.path.join(ROOT, "data", "pledge-counts.csv")

COUNTIES = ["Adair", "Adams", "Allamakee", "Appanoose", "Audubon", "Benton", "Black Hawk", "Boone", "Bremer",
            "Buchanan", "Buena Vista", "Butler", "Calhoun", "Carroll", "Cass", "Cedar", "Cerro Gordo", "Cherokee",
            "Chickasaw", "Clarke", "Clay", "Clayton", "Clinton", "Crawford", "Dallas", "Davis", "Decatur",
            "Delaware", "Des Moines", "Dickinson", "Dubuque", "Emmet", "Fayette", "Floyd", "Franklin", "Fremont",
            "Greene", "Grundy", "Guthrie", "Hamilton", "Hancock", "Hardin", "Harrison", "Henry", "Howard",
            "Humboldt", "Ida", "Iowa", "Jackson", "Jasper", "Jefferson", "Johnson", "Jones", "Keokuk", "Kossuth",
            "Lee", "Linn", "Louisa", "Lucas", "Lyon", "Madison", "Mahaska", "Marion", "Marshall", "Mills",
            "Mitchell", "Monona", "Monroe", "Montgomery", "Muscatine", "O'Brien", "Osceola", "Page", "Palo Alto",
            "Plymouth", "Pocahontas", "Polk", "Pottawattamie", "Poweshiek", "Ringgold", "Sac", "Scott", "Shelby",
            "Sioux", "Story", "Tama", "Taylor", "Union", "Van Buren", "Wapello", "Warren", "Washington", "Wayne",
            "Webster", "Winnebago", "Winneshiek", "Woodbury", "Worth", "Wright"]


def key(name):
    s = str(name or "").lower().replace("’", "'")
    s = re.sub(r"\bcounty\b", "", s)
    return re.sub(r"[^a-z']", "", s)


LOOKUP = {key(c): c for c in COUNTIES}


def find_county(payload):
    """Find a county anywhere in the event payload, whatever shape the sender used."""
    try:
        data = json.loads(payload)
    except (TypeError, ValueError):
        data = payload
    stack = [data]
    while stack:
        v = stack.pop()
        if isinstance(v, dict):
            stack.extend(v.values())
        elif isinstance(v, list):
            stack.extend(v)
        elif isinstance(v, str):
            if key(v) in LOOKUP:
                return LOOKUP[key(v)]
            t = v.strip()
            if t[:1] in "{[":
                try:
                    stack.append(json.loads(t))
                except ValueError:
                    pass
    return None


def describe(payload):
    """Summarize what was sent for the public run log, without showing emails or long answers."""
    try:
        data = json.loads(payload)
    except (TypeError, ValueError):
        data = payload

    def show(v):
        if isinstance(v, dict):
            return "{" + ", ".join(f"{k}: {show(x)}" for k, x in v.items()) + "}"
        if isinstance(v, list):
            return "[" + ", ".join(show(x) for x in v) + "]"
        t = str(v)
        if "@" in t or len(t) > 30:
            return f"<{len(t)} characters hidden>"
        return repr(t)

    return show(data)[:300]


def read_log():
    """Return [(date or None, county)], skipping lines that aren't a known county."""
    rows = []
    if not os.path.exists(LOG):
        return rows
    with open(LOG, newline="", encoding="utf-8-sig") as f:
        for i, r in enumerate(csv.reader(f)):
            if not r or (i == 0 and r[0].strip().lower() == "date"):
                continue
            county = LOOKUP.get(key(r[1] if len(r) > 1 else ""))
            if not county:
                print(f"::warning::Skipped log line {i + 1}: county not recognized ({r!r})")
                continue
            try:
                day = datetime.date.fromisoformat(r[0].strip())
            except ValueError:
                day = None
            rows.append((day, county))
    return rows


def write_log(rows):
    with open(LOG, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["date", "county"])
        for day, county in rows:
            w.writerow([day.isoformat() if day else "", county])


def write_counts(rows, today):
    cutoff = today - datetime.timedelta(days=30)
    total = {c: 0 for c in COUNTIES}
    recent = {c: 0 for c in COUNTIES}
    last = None
    for day, county in rows:
        total[county] += 1
        if day:
            if day >= cutoff:
                recent[county] += 1
            if last is None or day > last:
                last = day
    last_txt = f"{last.strftime('%b')} {last.day}, {last.year}" if last else ""
    with open(COUNTS, "w", newline="", encoding="utf-8") as f:
        f.write("county,individuals,organizations,new_30_days,last_pledge\n")
        w = csv.writer(f, lineterminator="\n")
        for c in COUNTIES:
            w.writerow([c, total[c], 0, recent[c], last_txt])
    return sum(total.values()), sum(1 for c in COUNTIES if total[c])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--add", default="", help="county to add one pledge for")
    ap.add_argument("--payload", default="", help="raw event payload (JSON) to search for a county")
    ap.add_argument("--date", default="", help="today's date (YYYY-MM-DD); defaults to the system date")
    a = ap.parse_args()
    today = datetime.date.fromisoformat(a.date) if a.date else datetime.date.today()

    rows = read_log()
    payload = a.payload.strip()
    if payload in ("null", "{}", '""'):
        payload = ""
    if a.add.strip() or payload:
        county = LOOKUP.get(key(a.add)) or find_county(payload)
        if county:
            rows.append((today, county))
            print(f"Added one pledge for {county} County on {today}.")
        else:
            got = describe(a.add.strip() or payload)
            print(f"::warning::No pledge added: no county found in what was sent ({got}). Totals were only recalculated.")
    rows.sort(key=lambda r: (r[0] or datetime.date.min, r[1]))
    write_log(rows)
    n, counties = write_counts(rows, today)
    print(f"{n} pledges in {counties} of 99 counties.")


if __name__ == "__main__":
    sys.exit(main())
