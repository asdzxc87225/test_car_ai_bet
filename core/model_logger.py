# core/model_logger.py

import json
from pathlib import Path
from datetime import datetime

LOG_PATH = Path("data/models/model_log.json")

def log_model(info: dict):
    """
    將訓練結果 info 記錄到 model_log.json
    每筆包含：參數、績效、timestamp
    """
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    if LOG_PATH.exists():
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []

    info["timestamp"] = datetime.now().isoformat()
    logs.append(info)

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

