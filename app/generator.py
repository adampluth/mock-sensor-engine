import numpy as np
from datetime import datetime

def generate_item_from_mode(mode_config: dict) -> dict:
    def noisy_value(param): return np.random.normal(param['base'], param['noise'])

    return {
        "product_id": "MOCK-001",
        "type": "MockType",
        "air_temperature": int(noisy_value(mode_config['air_temperature'])),
        "process_temperature": int(noisy_value(mode_config['process_temperature'])),
        "rotational_speed": int(noisy_value(mode_config['rotational_speed'])),
        "torque": int(noisy_value(mode_config['torque'])),
        "tool_wear": int(noisy_value(mode_config['tool_wear'])),
        "machine_failure": int(mode_config['machine_failure']),
    }
