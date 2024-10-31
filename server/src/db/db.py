from typing import List
from sqlmodel import SQLModel, Session, create_engine, select
from src.db.models import EnrichedDataModel, WeatherDataModel
from src.models.enriched_data import EnrichedData, WeatherData
from src.config import settings

engine = create_engine(settings.DB_URI)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def getAllData(size: int) -> List[EnrichedData]:
    with Session(engine) as session:
        # Get last size elements from the database, sorted by timestamp, latest first
        enrichedData = session.exec(select(EnrichedDataModel).order_by(EnrichedDataModel.timestamp.desc()).limit(size)).all()
        return [
            EnrichedData(
                **data.model_dump(),
                weather=WeatherData(
                    **session.get(WeatherDataModel, data.timestamp).model_dump()
                )
            )
            for data
            in enrichedData
        ]


def getDataByTimestamp(timestamp: int) -> EnrichedData:
    with Session(engine) as session:
        data = session.get(EnrichedDataModel, timestamp)
        if data is None:
            return None
        return EnrichedData(
            **data.model_dump(),
            weather=WeatherData(
                **session.get(WeatherDataModel, data.timestamp).model_dump()
            )
        )


def insertEnrichedData(enrichedData: EnrichedData) -> int:
    with Session(engine) as session:
        # convert weather data to WeatherDataModel
        weatherData = WeatherDataModel(
            timestamp=enrichedData.timestamp, temperature=enrichedData.weather.temperature, condition=enrichedData.weather.condition)
        session.add(weatherData)
        session.commit()
        session.refresh(weatherData)
        # convert enriched data to EnrichedDataModel
        enrichedDataModel = EnrichedDataModel(
            timestamp=enrichedData.timestamp,
            datetime=enrichedData.datetime,
            temperature=enrichedData.temperature,
            roomActivity=enrichedData.roomActivity,
            weatherTimestamp=weatherData.timestamp
        )
        session.add(enrichedDataModel)
        session.commit()
        session.refresh(enrichedDataModel)
        return enrichedDataModel.timestamp


def deleteData(timestamp: int) -> int:
    with Session(engine) as session:
        data = session.get(EnrichedDataModel, timestamp)
        weather = session.get(WeatherDataModel, timestamp)
        session.delete(data)
        session.delete(weather)
        session.commit()
        return timestamp
