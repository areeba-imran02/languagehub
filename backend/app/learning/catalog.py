import json
from pathlib import Path

_CATALOG = Path(__file__).resolve().parents[3] / "curriculum" / "modules.json"

def load_catalog():
    with _CATALOG.open(encoding="utf-8") as handle:
        return json.load(handle)
