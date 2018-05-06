Backend configuration
---------------------

Backend can be configured using environment variables. All of them follow below pattern:

```text
MEDTAGGER__[NAMESPACE]_[ENTRY-NAME]
```

**Note:** `MEDTAGGER` prefix follows by **two** underscores but after the namespace there
 is only **one** underscore!

### Current variables

Current configuration variables are:

| Environment variable name               | Default value                                              |
| --------------------------------------- | ---------------------------------------------------------- |
| `MEDTAGGER__API_HOST`                   | 0.0.0.0                                                    |
| `MEDTAGGER__API_REST_PORT`              | 51000                                                      |
| `MEDTAGGER__API_WEBSOCKET_PORT`         | 51001                                                      |
| `MEDTAGGER__API_DEBUG`                  | 1                                                          |
| `MEDTAGGER__API_SECRET_KEY`             | SECRET_KEY                                                 |
| `MEDTAGGER__DB_DATABASE_URI`            | postgresql://medtagger_user:MedTa99er!@localhost/medtagger |
| `MEDTAGGER__DB_CONNECTION_POOL_SIZE`    | 25                                                         |
| `MEDTAGGER__CASSANDRA_ADDRESSES`        | localhost                                                  |
| `MEDTAGGER__CASSANDRA_PORT`             | 9042                                                       |
| `MEDTAGGER__CELERY_BROKER`              | pyamqp://guest:guest@localhost//                           |

Default values are applied by `scripts/dev__configuration.sh` script that runs inside of
 `devenv.sh` script.

