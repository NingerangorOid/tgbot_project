import sqlite3
import csv


def connect_db(db_filename):
    return sqlite3.connect(db_filename)


def query_worlds(db_filename, danger_levels, keyword):
    conn = connect_db(db_filename)
    c = conn.cursor()
    c.execute("CREATE TEMP TABLE DangerLevels(level INT)")
    for level in danger_levels:
        c.execute("INSERT INTO DangerLevels VALUES (?)", (level,))
    c.execute("""SELECT Worlds.id, Worlds.name, Dangers.danger, Dangers.character
                 FROM Worlds
                 JOIN Dangers ON Worlds.danger_id = Dangers.id
                 JOIN DangerLevels ON Dangers.level = DangerLevels.level
                 WHERE Worlds.name LIKE ?""", ('%' + keyword + '%',))
    selected_worlds = c.fetchall()
    conn.close()
    return selected_worlds


def write_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['no-world-danger-character'])
        for idx, row in enumerate(data, 1):
            writer.writerow([idx] + list(row))

#  28..03.2024https://github.com/NingerangorOid/tgbot_project.git

db_filename = input("Введите имя файла базы данных: ")
danger_levels = list(map(int, input("Введите уровни опасности через пробел: ").split()))
keyword = input("Введите слово в названии мира: ").strip().lower()
selected_worlds = query_worlds(db_filename, danger_levels, keyword)
write_to_csv(selected_worlds, 'snakehounds.csv')