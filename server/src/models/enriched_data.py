from pydantic import BaseModel


class WeatherData(BaseModel):
    temperature: float
    condition: str


class EnrichedData(BaseModel):
    timestamp: int
    datetime: str
    temperature: float
    roomActivity: str
    weather: WeatherData

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'timestamp': 1672531200,
                    'datetime': '2024-10-31 10:00:00',
                    'temperature': 99.99,
                    'roomActivity': 'working',
                    'weather': {
                        'temperature': 20.0,
                        'condition': 'clear sky'
                    }
                }
            ]
        }
    }
