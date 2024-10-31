from pydantic import BaseModel


class EspData(BaseModel):
    date: str
    time: str
    temperature: float

    # Add example data
    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'date': '2024-10-31',
                    'time': '10:00:00',
                    'temperature': 20.0
                }
            ]
        }
    }
