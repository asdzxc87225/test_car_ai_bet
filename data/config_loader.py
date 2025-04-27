import yaml
from pathlib import Path
def load_config():
    config_path = Path("config/data_config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def get_car_name_by_index(index: int, config: dict) -> str:
    return config["bet_vector"]["cars"].get(str(index), "未知車輛")

def get_car_index_by_name(name: str, config: dict) -> int:
    car_map = config["bet_vector"]["cars"]
    for idx, car_name in car_map.items():
        if car_name == name:
            return int(idx)
    return -1  # 沒找到
if __name__ == "__main__":
    #test
    config = load_config()
    print(get_car_name_by_index(2, config))  # 綠車
    print(get_car_index_by_name("紅車", config))  # 0


