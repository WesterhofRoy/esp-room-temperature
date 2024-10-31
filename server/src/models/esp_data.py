from pydantic import BaseModel


class EspData(BaseModel):
    time: int
    temperature: float

    # Add example data
    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'time': '1730407380',
                    'temperature': 20.0
                }
            ]
        }
    }
