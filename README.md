# Prosjekt-TDT4145 - Jernbane Billettbestillingssystem

Et omfattende billettbestillingssystem for jernbane utviklet for kurset TDT4145 ved NTNU. Systemet håndterer togårer, stasjoner, kunder og billettbestillinger for det norske jernbanenettverket, med fokus på Nordlandsbanen.

## 🚂 Funksjoner

- **Stasjonsadministrasjon**: Administrere jernbanestasjoner langs togruter
- **Ruteplanlegging**: Vise togruter og timeplaner mellom stasjoner
- **Kunderegistrering**: Registrere nye kunder med validering
- **Billettbestilling**: Bestille seter eller sovekupeer på tog
- **Kjøpshistorikk**: Vise kunders bestillingshistorikk
- **Sanntidstilgjengelighet**: Sjekke tilgjengelighet for seter og soveplasser

## 📁 Prosjektstruktur

Prosjekt-TDT4145/ ├── init.sql Databaseinitialisering med Nordlandsbanen-data 
                  ├── prosjektTDT4145_GR103.sql Databaseskjemadefinisjon 
                  ├── togprosjekt.py Hovedapplikasjon med full funksjonalitet 
                  ├── kopi.py Utviklings-/sikkerhetskopi-versjon 
                  ├── legge_inn_senger.py Innlegging av sovekupédata 
                  ├── legge_inn_seter.py Innlegging av setedata 
                  └── README.md # Denne filen

## 🗄️ Databaseskjema

Systemet bruker SQLite med følgende hovedtabeller:

- **Jernbanestasjon**: Jernbanestasjoner
- **Banestrekning**: Jernbanestrekninger
- **Delstrekning**: Delstrekninger av jernbanestrekninger
- **Togrute**: Togruter
- **Togreise**: Individuelle togreiser
- **Kunde**: Kundeinformasjon
- **Billett**: Billettinformasjon
- **Bestilling**: Bestillinger/ordre

## 🚀 Kom i gang

### Forutsetninger

- Python 3.x
- SQLite3 (inkludert med Python)

### Installasjon

1. Klon depotet:
```bash
git clone [https://github.com/hakongrue/Prosjekt-TDT4145.git](https://github.com/hakongrue/Prosjekt-TDT4145.git)
cd Prosjekt-TDT4145
