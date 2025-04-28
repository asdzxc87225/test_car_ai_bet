# data/global_data.py
from data.data_facade import DataFacade
from data.config_loader import load_config
from pathlib import Path

DATA_FACADE = DataFacade("data/raw/game_log.csv",'data/models/q_model_0425_2023.pkl')
CONFIG = load_config()
