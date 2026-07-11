# Wikidata-OSM Matcher

Webbapplikation för att matcha Wikidata-objekt mot OpenStreetMap med manuell validering.

## Översikt

Systemet hämtar objekt från Wikidata som saknar OSM-länk (P402), presenterar kandidater från Overpass API för matchning, och låter användaren bekräfta eller avvisa varje matchning.

## Arkitektur

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Vue/Vite  │────▶│   FastAPI   │────▶│  Wikidata   │
│  Frontend   │◀────│   Backend   │────▶│  (SPARQL)   │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Overpass   │
                    │    API      │
                    └─────────────┘
```

## Objekttyper

Matcheringsmetoderna konfigureras per objekttyp i YAML:

| Typ | Metod | Beskrivning |
|-----|-------|-------------|
| `hiking_trail` | name | Namnbaserad fuzzy match inom landets bbox |
| `bathing_place` | bbox | Geografisk sökning inom 1km radie från koordinater |

## Konfiguration

YAML-filer i `configs/`:

```yaml
object_type: hiking_trail
label: "Vandringsleder"

wikidata:
  sparql_query: |     # SPARQL för att hämta objekt utan P402
  overpass:
    query: |          # Overpass QL med {{bbox}} placeholder
  matching:
    method: name     # "name" eller "bbox"
    similarity_threshold: 0.3
    exclude_words: [...]
```

## Installation

### Backend

```bash
cd backend
poetry install
poetry run uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

| Method | Endpoint | Beskrivning |
|--------|----------|-------------|
| GET | `/api/types` | Lista objekttyper |
| GET | `/api/types/{type}/candidates` | Objekt som behöver matchas |
| GET | `/api/types/{type}/candidates/{qid}/matches` | OSM-kandidater för ett objekt |
| POST | `/api/types/{type}/candidates/{qid}/confirm` | Bekräfta matchning |
| POST | `/api/types/{type}/candidates/{qid}/reject` | Markera som "ingen match" |

## Wikidata OAuth

Skrivåtkomst till Wikidata kräver OAuth-autentisering. Konfigurera credentials i miljövariabler:

- `WIKIDATA_CONSUMER_KEY`
- `WIKIDATA_CONSUMER_SECRET`

## Lägga till ny objekttyp

1. Skapa `configs/{ny_typ}.yaml` med SPARQL-query och Overpass-fråga
2. Starta om backend
3. Ny typ dyker upp i webbgränssnittet

## Tech Stack

| Lager | Teknologi |
|-------|-----------|
| Backend | FastAPI, Pydantic, httpx |
| Frontend | Vue 3, Vite, TypeScript, Pinia |
| Matching | rapidfuzz (fuzzy string matching) |
| Wikidata | SPARQL + Wikibase API |
| OSM | Overpass API |
