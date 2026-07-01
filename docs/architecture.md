# ELEV Finance Agent Architecture

## Ziel

Der ELEV Finance Agent automatisiert die Verarbeitung von Finanzdokumenten, Belegen, Rechnungen und Buchungen.

## Schichten

```text
app/
├── api/             REST-Endpunkte
├── services/        Geschäftslogik
├── repositories/    Datenbankzugriff
├── models/          SQLAlchemy-Modelle
├── schemas/         Pydantic-Schemas
├── connectors/      Externe Systeme
├── database/        Datenbankverbindung
├── config/          Konfiguration
└── main.py          App-Einstieg