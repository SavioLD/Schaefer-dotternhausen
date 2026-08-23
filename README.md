# Karriere-Landingpage · Schäfer intelligente Haustechnik GmbH

Ad-Funnel / Karriereseite für **Schäfer intelligente Haustechnik GmbH**, Dotternhausen.
Aufbau **1:1 identisch zur ALWA-Seite** (`saviold/alwa-gmbh`) – nur im Schäfer-CI
(Rot `#d81f34` / Anthrazit) und mit den offenen SHK-Positionen.

Single-File-Seite: `index.html` (kein Build-Tool). Enthält Hero, Trust-Band,
3 Stellen, Benefits, Ablauf, mehrstufiges Bewerbungsformular (mit Screen-out &
optionalem Lebenslauf-Upload), FAQ und Footer.

## Offene Stellen
1. Technischer Systemplaner (m/w/d)
2. Technischer Zeichner (m/w/d)
3. Kaufmännisch-Technischer Sachbearbeiter (m/w/d) – mit Erfahrung in SHK

## Noch einzutragen (2 Dinge)

### 1. LeadTable-Webhook  ✅ verbunden
Verbundene Kachel:
`https://portal.lead-table.com/customer/69c6564fa939ff445ad9cb74/table/69c6566ba939ff445ad9d313/leads`

Der Generic-Webhook ist in `index.html` (`WEBHOOK_URL`) eingetragen – Bewerbungen
landen direkt in dieser Tabelle. Die Felder werden als JSON übergeben:
`vorname, nachname, name, email, telefon, stelle, erfahrung, lebenslauf,
datenschutz, quelle, seite`.

### 2. Logo & Fotos (optional, aber empfohlen)
Dateien in `bilder/` ablegen – werden automatisch erkannt:
- Logo: `schaefer-logo.svg` (Header/Footer, farbig) und
  `schaefer-logo-weiss.svg` (Hero, weiß). Solange keins vorhanden ist, greift
  der Text-Schriftzug „Schäfer".
- Hero-Foto: `hero.jpg` (allgemein) bzw. `hero-systemplaner.jpg`,
  `hero-zeichner.jpg`, `hero-sachbearbeiter.jpg` pro Stelle. Ohne Foto bleibt
  der rote Markenverlauf stehen.

## Deep-Links pro Stelle (für Ads)
`?stelle=systemplaner` · `?stelle=zeichner` · `?stelle=sachbearbeiter`
– setzt Hero-Titel + Formular direkt auf die gewählte Position.

## Lebenslauf-Upload
Läuft über den geteilten Ländle-Digital-Supabase-Bucket `bewerbungen`
(öffentlich, aber nur per zufälliger UUID-URL erreichbar) – funktioniert ohne
weitere Einrichtung.

## Lokal ansehen
```bash
python3 -m http.server 8000
# → http://localhost:8000/kunden/schaefer-dotternhausen/
```
