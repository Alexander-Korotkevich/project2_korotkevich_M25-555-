import functools
import prompt


def handle_db_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(
                "Ошибка: Файл данных не найден. Возможно, база данных не инициализирована."
            )
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

    return wrapper


def confirm_action(action_name: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            user_input = prompt.string(
                f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            )
            if user_input.lower() == "y":
                return func(*args, **kwargs)
            else:
                print("Действие отменено.")

        return wrapper

    return decorator


def log_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import time

        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        # Форматирование времени
        elapsed = end_time - start_time
        print(f"Функция {func.__name__} выполнилась за {elapsed:.4f} секунд")
        return result

    return wrapper
