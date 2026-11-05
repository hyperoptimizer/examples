import json
from pathlib import Path
import tomllib
import jsonschema

root = Path(__file__).resolve().parents[1]
schema = json.loads((root / "contracts/hpo-config.json").read_text())
for path in root.rglob("hpo.toml"):
    config = tomllib.loads(path.read_text())
    jsonschema.validate(config, schema)
    print("Valid:", path.relative_to(root))
