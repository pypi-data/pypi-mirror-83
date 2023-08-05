![GitHub top language](https://img.shields.io/github/languages/top/marcuxyz/flore) ![GitHub](https://img.shields.io/github/license/marcuxyz/flore) ![GitHub repo size](https://img.shields.io/github/repo-size/marcuxyz/flore)

It's a script to transform yaml file to SQL-code.

We worked as a migration to the database. You can create your migration through of migration.yaml file inside migrations folder and run the script for migrate.

# Install

You can install the script through of pip command:

```bash
pip intall flore
```

# Usage

Run the command `flore init` to create `migration` folder with the follow files:

- migration.yaml
- seed.yaml
- config.yaml

# Configuration

For configuration the `migration`, open `config.yaml` file and set information:

```yaml
dialect: 'pg'
host: 'localhost'
port: 5432
username: 'postgres'
password: 'docker'
database: 'flore'
```

`dialect` is a name of the database service, for example: mysql, pg => postgres. Currently support `postgres` only. Now,
you can set `username`, `password`, `database`, `port` and `host` for you database.


# Migration

For create migration you set in migration.yaml the following information:

```yaml
tables:
  users:
    name:
      - varchar:120
      - required
    email:
      - varchar:84
      - required
      - unique
    password:
      - varchar:255
    is_admin:
      - boolean
      - default false
  products:
    price:
      - float
```

Run with the follow command

```yaml
flore run
```

To migrate tables your postgres database.

# Screenshot

![migration.yaml](https://pbs.twimg.com/media/EkxpbhqWkAAmh_R?format=jpg&name=medium)
![SQL1](https://pbs.twimg.com/media/EkxpckQXUAIYIhg?format=jpg&name=medium)
![SQL2](https://pbs.twimg.com/media/EkxqWIdWkAIzfXi?format=jpg&name=medium)
