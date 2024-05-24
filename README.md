# hai-cloud-web

This is for my new company's website.

Still developing.

Subfolder `pgdata/` is needed for postgreSQL.

```
docker compose up -d db
# after if finishs creating the database from scratch
python .\init_database.py
docker compose logs -f django
```