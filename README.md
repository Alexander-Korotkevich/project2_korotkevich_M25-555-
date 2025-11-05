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

## CRUD-операции

### INSERT

`insert into <имя_таблицы> values (<значение1>, <значение2>, ...)`

##### Пример

`insert into table1 values(alex, 22, False)`

### SELECT

`select from <имя_таблицы> where <столбец> = <значение>`

или

`select from <имя_таблицы>` - если нужно выбрать **все** записи

##### Пример

`select from table1 where age = 22`

### UPDATE

`update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия>`

##### Пример

`update table1 set age = 32 where name = 'alex'`

### DELETE

`delete from <имя_таблицы> where <столбец> = <значение>`

##### Пример

`delete from table1 where age = 32`


[![Demo](https://asciinema.org/a/osqIhSAMg6K7cc5lkgQcnDl5T.svg)](https://asciinema.org/a/osqIhSAMg6K7cc5lkgQcnDl5T)
