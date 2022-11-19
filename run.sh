export MONGO_URL=mongodb://mongoadmin:L4N61N6@mongo:27017/?authMechanism=DEFAULT
export MONGO_DB_NAME=langing
export MINUTES=43200
export ANALYTIC_ID=de4ffebd-f08c-44dd-96a2-c063903682dd

docker build -t langing-crawler .

docker run --rm  --network local-network \
  --name crawler-local \
  -eMONGO_URL=$MONGO_URL -eANALYTIC_ID=$ANALYTIC_ID -eMINUTES=$MINUTES \
  langing-crawler