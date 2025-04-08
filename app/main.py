from fastapi import FastAPI, WebSocket, APIRouter
from typing import List
from datetime import datetime
import asyncio

from .config import load_mode
from .models import SensorConfig
from .generator import generate_item_from_mode

app = FastAPI()
router = APIRouter()


# --- Route: Simulate a single data point from a mode ---
@router.get("/simulate/{mode_name}")
def simulate_sensor_data(mode_name: str):
    mode = load_mode(mode_name)
    return generate_item_from_mode(mode)


# --- Route: Generate once using raw sensor config (for manual POST testing) ---
@app.post("/generate-once")
def generate_once(sensors: List[SensorConfig]):
    t = datetime.utcnow().timestamp()
    
    def generate_sensor_reading(config: SensorConfig, t: float):
        import numpy as np
        wave = (
            np.sin(2 * np.pi * config.sine_freq * t) * config.sine_amplitude
            if config.sine_freq and config.sine_amplitude else 0
        )
        noise = np.random.normal(0, config.noise_std)
        value = config.base_value + wave + noise
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "name": config.name,
            "value": value,
        }

    return [generate_sensor_reading(config, t) for config in sensors]


# --- Route: WebSocket stream (real-time) using hardcoded SensorConfig ---
@app.websocket("/stream")
async def stream(websocket: WebSocket):
    await websocket.accept()
    sensors = [
        SensorConfig(name="rpm", base_value=3600, noise_std=5, sine_freq=0.01, sine_amplitude=50),
        SensorConfig(name="temp", base_value=75, noise_std=0.5, sine_freq=0.005, sine_amplitude=3),
    ]

    def generate_sensor_reading(config: SensorConfig, t: float):
        import numpy as np
        wave = (
            np.sin(2 * np.pi * config.sine_freq * t) * config.sine_amplitude
            if config.sine_freq and config.sine_amplitude else 0
        )
        noise = np.random.normal(0, config.noise_std)
        value = config.base_value + wave + noise
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "name": config.name,
            "value": value,
        }

    while True:
        t = datetime.utcnow().timestamp()
        readings = [generate_sensor_reading(config, t) for config in sensors]
        await websocket.send_json(readings)
        await asyncio.sleep(1)


# --- Mount router for mode-based simulation ---
app.include_router(router)
