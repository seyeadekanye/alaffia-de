# alaffia-de

### Setting up the project
From the base bath, i.e. the same directory as the docker compose file, run the following:
- docker-compose build
- docker-compose up -d
- docker-compose exec web python coinr/manage.py migrate --noinput
- docker-compose run --rm -w /opt/app/coinr web python manage.py runserver

### Sending Traffic to the server
- The server expects to receive post requests to localhost:8080/api/coin-task/

### Database
A postgres sevrer was provisioned as part of docker-compose with the following credentials
- dbname: coinr
- user: alaffia
- password: password
- port: 5432
- host: localhost

### Brief walk through of implementation
Because of the requirement fo a 400ms response time, it was clear that the server will have to process this requests
asynchronously. To achieve this, I decided to utilize redis as a message brokwr and celery to be able to run background tasks. Celery
will also be used as a way to handle the throttling from CoinGecko for later retires.

