import yaml

def load_mode(mode_name: str, filepath="config/modes.yaml"):
    with open(filepath, "r") as f:
        modes = yaml.safe_load(f)
    return modes[mode_name]
