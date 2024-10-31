from sqlmodel import SQLModel, Field


class WeatherDataModel(SQLModel, table=True):
    timestamp: int = Field(primary_key=True)
    temperature: float
    condition: str


class EnrichedDataModel(SQLModel, table=True):
    timestamp: int = Field(primary_key=True)
    datetime: str
    temperature: float
    roomActivity: str
    weatherTimestamp: int = Field(foreign_key="weatherdatamodel.timestamp")
