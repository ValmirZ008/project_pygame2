import sqlite3


def init_db():
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            best_score INTEGER DEFAULT 0
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            menu_volume INTEGER DEFAULT 50,
            level_music_volume INTEGER DEFAULT 50,
            effects_volume INTEGER DEFAULT 50
        )
        """
    )
    cursor.execute("SELECT COUNT(*) FROM settings")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO settings (menu_volume, level_music_volume, effects_volume) VALUES (50, 50, 50)"
        )
    cursor.execute("SELECT COUNT(*) FROM scores")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO scores (best_score) VALUES (0)")
    conn.commit()
    conn.close()


def get_best_score():
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT best_score FROM scores LIMIT 1")
    result = cursor.fetchone()
    best_score = result[0] if result else 0
    conn.close()
    return best_score


def update_best_score(new_score):
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE scores SET best_score = ? WHERE best_score < ?", (new_score, new_score)
    )
    conn.commit()
    conn.close()


def get_settings():
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT menu_volume, level_music_volume, effects_volume FROM settings LIMIT 1"
    )
    settings = cursor.fetchone()
    conn.close()
    return settings if settings else (50, 50, 50)


def update_settings(menu_volume, level_music_volume, effects_volume):
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE settings SET menu_volume = ?, level_music_volume = ?, effects_volume = ?",
        (menu_volume, level_music_volume, effects_volume),
    )
    conn.commit()
    conn.close()
    return menu_volume, level_music_volume, effects_volume
