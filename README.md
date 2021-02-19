[![Yamdb_final workflow](https://github.com/backdev96/yamdb_final/workflows/Yamdb-app_workflow/badge.svg)](https://github.com/backdev96/yamdb_final/actions)

Author: Efremov Stanislav

Built with:

- Python 3.8
- Django
- Django Rest Framework
- PostgreSQL
- Docker
- nginx

Build and run your app with Compose:

    1) docker-compose build

    2) docker-compose up

Perform migrations:

    docker-compose run web python manage.py migrate

Database load data command:

    docker-compose run web python manage.py loaddata fixtures.json

Superuser creation:

    docker-compose run web python manage.py createsuperuser

