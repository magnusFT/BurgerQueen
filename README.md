# Burger Queen Applikasjon

Dette er en enkel "Burger Queen" applikasjon som lar brukere logge inn, lage kontoer, lage bestillinger og vise bestillinger. Applikasjonen bruker SQLite som databasen for lagring av brukerinformasjon, burgere, ingredienser og bestillinger. Skoleprosjekt Tiller vgs IT2

## Funksjonalitet

### 1. Lage en database

Første gang du kjører programmet, vil det opprette en SQLite-database (`BurgerQueenSql.db`) og legge til dummydata ved hjelp av SQL-skriptet (`dummydatasqlscript.sql`).

### 2. Logg Inn

- Velg "1" fra hovedmenyen for å logge inn.
- Skriv inn brukernavn og passord når du blir bedt om det.
- Hvis autentiseringen er vellykket, blir du dirigert til enten ansattmenyen eller kundemenyen, avhengig av brukertype.

### 3. Lage Konto

- Velg "2" fra hovedmenyen for å opprette en ny konto.
- Skriv inn ønsket brukernavn og passord.
- Velg om kontoen skal være en ansattkonto eller ikke.

### 4. Ansatt Meny

- Hvis du logger inn med en ansattkonto, vil du se følgende alternativer:
  - "1. Vis Bestillinger": Viser alle bestillinger i systemet.
  - "2. Lage en Bestilling": Gir ansatte muligheten til å legge til en ny bestilling.
  - "3. Logg Ut": Logger deg ut og tar deg tilbake til hovedmenyen.

### 5. Kundemeny

- Hvis du logger inn med en kundekonto, vil du se følgende alternativer:
  - "1. Lage en Bestilling": Gir kunder muligheten til å legge til en ny bestilling.
  - "2. Logg Ut": Logger deg ut og tar deg tilbake til hovedmenyen.

### 6. Lage en Bestilling

- Velg "1" fra kundemenyen eller ansattmenyen for å lage en ny bestilling.
- Velg burgeren du ønsker å bestille fra listen.
- Bestillingen blir lagt til i databasen.

## Avslutte Programmet

- Velg "3" fra hovedmenyen for å avslutte programmet.



