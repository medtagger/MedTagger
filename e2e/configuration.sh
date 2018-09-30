export MEDTAGGER__API_HOST="0.0.0.0"
export MEDTAGGER__API_REST_PORT=51000
export MEDTAGGER__API_WEBSOCKET_PORT=51001
export MEDTAGGER__API_DEBUG=1
export MEDTAGGER__API_SECRET_KEY="SECRET_KEY"

export MEDTAGGER__DB_DATABASE_URI="postgresql://medtagger_user:MedTa99er!@127.0.0.1:52002/medtagger"
export MEDTAGGER__DB_CONNECTION_POOL_SIZE=10

export MEDTAGGER__CASSANDRA_ADDRESSES="127.0.0.1"
export MEDTAGGER__CASSANDRA_PORT=52001
export MEDTAGGER__CASSANDRA_DEFAULT_TIMEOUT=30
export MEDTAGGER__CASSANDRA_CONNECT_TIMEOUT=30

export MEDTAGGER__CELERY_BROKER="pyamqp://guest:guest@127.0.0.1//"

