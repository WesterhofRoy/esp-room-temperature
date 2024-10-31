from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from src.models.esp_data import EspData
from src.models.enriched_data import EnrichedData
from src.helpers.enrich_helper import enrichEspData
from src.db import db
from src.db.models import *
from src.config import log

app = FastAPI()

db.create_db_and_tables()


@app.get('/data')
def getDbData(size: Optional[int] = 10) -> List[EnrichedData]:
    log.info('Getting all data')
    result = db.getAllData(size)
    log.debug(f'Got {len(result)} records')
    log.info('Successfully retrieved all data')
    return result


@app.get('/data/{timestamp}')
def getDbDataByTimestamp(timestamp: int) -> EnrichedData:
    log.info('Getting data by timestamp')
    result = db.getDataByTimestamp(timestamp)
    if result is None:
        log.info('Data not found')
        raise HTTPException(status_code=404, detail='Data not found')
    log.debug('Successfully retrieved data')
    return result


@app.post('/data', status_code=status.HTTP_201_CREATED)
def postDbData(data: EspData):
    log.info('Posting ESP data')
    log.debug('Enriching data')
    enrichedData = enrichEspData(data)
    log.debug('Data enriched')
    log.debug('Inserting enriched data into database')
    result = db.insertEnrichedData(enrichedData)
    log.info('Successfully posted ESP data')
    return result


@app.post('/data/bulk', status_code=status.HTTP_201_CREATED)
def postBulkDbData(data: List[EspData]):
    log.info('Posting bulk ESP data')
    for item in data:
        postDbData(item)
    log.debug(f'{len(data)} records posted')
    log.info('Successfully posted bulk ESP data')


@app.post('/data/bulk/enriched', status_code=status.HTTP_201_CREATED)
def postBulkEnrichedData(data: List[EnrichedData]):
    log.info('Posting bulk enriched data')
    for item in data:
        db.insertEnrichedData(item)
    log.debug(f'{len(data)} records posted')
    log.info('Successfully posted bulk enriched data')


@app.delete('/data/{timestamp}', status_code=status.HTTP_204_NO_CONTENT)
def deleteData(timestamp: int):
    log.info('Deleting data')
    db.deleteData(timestamp)
    log.info('Successfully deleted data')
