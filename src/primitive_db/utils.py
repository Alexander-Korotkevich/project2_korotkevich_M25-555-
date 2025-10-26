import json


def load_metadata(filepath: str):
    """Загрузка данных из файла"""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None


def save_metadata(filepath: str, data) -> bool:
    """Сохранение данных в файл"""
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)
            return True
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
        return False
