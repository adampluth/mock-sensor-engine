from fastapi import FastAPI, WebSocket, APIRouter, Query
from typing import List
from datetime import datetime
from uuid import uuid4
import asyncio
import numpy as np

from .config import load_mode
from .models import SensorConfig
from .generator import generate_item_from_mode
from .scheduler import mode_schedule_generator

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

# --- Updated: WebSocket stream with session ID, unique ID, and override support ---
@app.websocket("/stream")
async def stream(
    websocket: WebSocket,
    session_id: str = Query(default_factory=lambda: f"mock-{uuid4().hex[:6]}"),
    mode_override: str = Query(default=None)
):
    await websocket.accept()
    scheduler = mode_schedule_generator()

    while True:
        current_mode = mode_override or next(scheduler)
        mode_config = load_mode(current_mode)
        item = generate_item_from_mode(mode_config)

        message = {
            "id": str(uuid4()),
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat(),
            "mode": current_mode,
            "data": item
        }

        await websocket.send_json(message)
        await asyncio.sleep(1)

# --- Mount router for mode-based simulation ---
app.include_router(router)
