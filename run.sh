export MONGO_URL=mongodb://mongoadmin:L4N61N6@mongo:27017/?authMechanism=DEFAULT
export MONGO_DB_NAME=langing
export MINUTES=60
export ANALYTIC_ID=a21e48e4-9d11-4457-8710-9e1f62f26f27

docker build -t langing-crawler .

docker run --rm  --network local-network \
  --name crawler-local \
  -eMONGO_URL=$MONGO_URL -eANALYTIC_ID=$ANALYTIC_ID -eMINUTES=$MINUTES \
  langing-crawler