MODE_SEQUENCE = [
    ("idle", 10),
    ("startup", 10),
    ("steady_state", 20),
    ("degrading", 15),
    ("failure", 10),
]

def mode_schedule_generator():
    while True:
        for mode, duration in MODE_SEQUENCE:
            for _ in range(duration):
                yield mode
