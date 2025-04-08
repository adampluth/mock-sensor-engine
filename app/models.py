from pydantic import BaseModel
from typing import Optional

class SensorConfig(BaseModel):
    name: str
    base_value: float
    noise_std: float
    sine_freq: Optional[float] = None
    sine_amplitude: Optional[float] = None

class SensorReading(BaseModel):
    timestamp: str
    name: str
    value: float
