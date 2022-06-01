import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.db.models import F

from .models import CoinTask, TaskCount

logger = get_task_logger(__name__)

COIN_GECKO_BASE_ENDPOINT = 'https://api.coingecko.com/api/v3/coins/'

def get_and_increment_task_id():
    task_counter = TaskCount.objects.get_or_create(id='taskr-counter')
    task_id = task_counter.counter
    task_counter.update(counter=F('counter')+1)
    return task_id

@shared_task
def handle_csv(data):
    logger.info('handing off to celery')
    logger.info(data)
    try:
        ids = data[1:]
        for id in ids:
            if CoinTask.objects.filter(id=id).exists():
                logger.info(f'id already exists in the database')
                break
            response = requests.get(COIN_GECKO_BASE_ENDPOINT + f'{id}/tickers')
            if response.status_code == 404:
                logger.exception(f'Coin does not exist. id: {id}')
            elif response.status_code == 429:
                logger.info(f'Requests are being throttles')
            elif response.status_code == 200:
                data = response.json()
                tickers = data.get('tickers')
                tickers_list = [t.get('market').get('identifier') for t in tickers]
                logger.info(tickers_list)
                CoinTask(
                    id=id,
                    exchanges=tickers_list,
                    task_id=get_and_increment_task_id()
                ).save()
            else:
                logger.error(f'There was an issue fetching data for id: {id}')
    except Exception as e:
        pass


@shared_task
def handle_json(data):
    logger.info('handing off to celery')
    logger.info(data)
    try:
        ids = data.get('coins')
        for id in ids:
            if CoinTask.objects.filter(id=id).exists():
                logger.info(f'id already exists in the database')
                break
            response = requests.get(COIN_GECKO_BASE_ENDPOINT + f'{id}/tickers')
            if response.status_code == 404:
                logger.exception(f'Coin does not exist. id: {id}')
            elif response.status_code == 429:
                logger.info(f'Requests are being throttled')
            elif response.status_code == 200:
                data = response.json()
                logger.info(data)
                tickers = data.get('tickers')
                tickers_list = [t.get('market').get('identifier') for t in tickers]
                logger.info(tickers_list)
                CoinTask(
                    id=id,
                    exchanges=tickers_list,
                    task_id=get_and_increment_task_id()
                ).save()
            else:
                logger.error(f'There was an issue fetching data for id: {id}')
    except Exception as e:
        pass