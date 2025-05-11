### Konfigruacja 
Utworzenie na sqlitecloud.io bazy danych fraud_database i wykonanie na niej skryptu sql/create_table_archived_clames.sql.
Po utworzeniu bazy dnaych connection string jest dostępny na https://sqlitecloud.io/.

Utworzenie na projektu fraud_oracle na wandb.
Po utworzeniu projektu fraud_oracle klucz api jest dostęny na https://wandb.ai/

GOOGLE_CREDENTIALS: /run/keys/engineering-thesis.json
Dostęny do konta usług w pliku json

AUTH_LOGIN: a
Login którym mają przedstawiać się żadania predykcji.

AUTH_PASSWORD: a
Hasło którym mają przedstawiać się żadania predykcji.

MODEL_ID: 3f12e56b
Id modelu prdeykcji na którym działa aplikacja.

TEST_DATA_ID: ca458f5c
Id danych testowych potrzebnych do wygenerowania raportu DataDrift.

SQL_CONNESCTION: sqlitecloud://crauyqqhnz.g6.sqlite.cloud:8860/fraud_database?apikey=key
Connection string do sqlitecloud.

COLLECT_CLAIMS: true
Czy aplikacja ma zapisywac żadania predykcji (razem z predykcją) na sqlitecloud.

COLLECT_METRICS: true
Czy aplikacja ma generować raport DataDrift.

MAX_INSERT_CLAIM_WORKERS: 20
Ilośc wątków umieszczających żadania predykcji do sqlitecloud.

CLAIMS_LIMIT: 3000
Max ilość pobranych najnowszych żądań predykcji z bazy danych.

METRICS_SCHEDULER_INTERVAL_MINUTES: 60
Co ile minut aport DataDrift ma być generowany.

WANDB_API_KEY: a
Klucz do wandb

Przykład docker-compose_example.yml

### Budowa obrazu:
docker-compose build
 
### Start aplikacji
docker-compose up 
