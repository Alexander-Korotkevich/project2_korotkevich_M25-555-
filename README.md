# База данных

## 🚀 Быстрый старт

#### Установка

`poetry install` или `make install`

### Запуск

`database`

<hr />

## Управление таблицами

#### Создание таблицы

`create_table <имя_таблицы> <столбец1:тип> ..`

##### Пример:

`create_table users first_name:str last_name:str age:int is_student:bool`

В результате будет создана таблица **users** с колонками: **ID (int)**, **first_name (str)**, **last_name (str)**, **age (int)**, **is_student (bool)**

#### Удаление таблицы

`drop_table <имя_таблицы>`

##### Пример:

`drop_table users`

В результате будет удалена таблица **users**

#### Список таблиц

`list_tables`

В результате будет показан список таблиц:

```
Список таблиц:
table1,
table2,
...
```

[![Demo](https://asciinema.org/a/EbDWyR28r1ZMx8eJrvZ4cseOs.svg)](https://asciinema.org/a/EbDWyR28r1ZMx8eJrvZ4cseOs)

<hr />
