# user_management.py
import sqlite3
from database import get_connection

def register_user(username, password, is_superuser=0):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM Users WHERE username = ?", (username,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return False, "Пользователь с таким логином уже существует."

    cursor.execute("""
        INSERT INTO Users (username, password, is_superuser)
        VALUES (?, ?, ?)
    """, (username, password, is_superuser))
    conn.commit()
    conn.close()
    return True, "Пользователь успешно зарегистрирован."

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, is_superuser FROM Users WHERE username = ?", (username,))
    user_row = cursor.fetchone()
    conn.close()

    if not user_row:
        return None, "Неправильный логин."
    user_id, db_username, db_password, db_superuser = user_row

    if password != db_password:
        return None, "Неверный пароль."

    return {
        "id": user_id,
        "username": db_username,
        "is_superuser": db_superuser
    }, "Успешный вход"

def change_password(user_id, old_password, new_password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM Users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False, "Пользователь не найден."

    current_password = row[0]
    if current_password != old_password:
        conn.close()
        return False, "Старый пароль неверен."

    cursor.execute("UPDATE Users SET password = ? WHERE id = ?", (new_password, user_id))
    conn.commit()
    conn.close()
    return True, "Пароль успешно изменён."
