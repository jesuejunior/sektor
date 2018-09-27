# encoding: utf-8
import sqlite3
from datetime import datetime


class DB:
    def connect():
        conn = sqlite3.connect("sektor.db")
        return conn

    def init():
        conn = DB.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS track (time INTEGER,
                lat DOUBLE PRECISION, lon DOUBLE PRECISION,
                speed INT, distance INT, oil BOOLEAN, created_at DATETIME)"""
            )
            conn.commit()
        finally:
            conn.close()
        return True

    def find_last_position():
        conn = DB.connect()
        cursor = conn.cursor()
        try:
            result = cursor.execute(
                """select * from track order by created_at DESC limit 1"""
            )
            return result[0] if len(result) else False
        except Exception as ex:
            print(ex)
            return False
        finally:
            conn.close()

        return True

    def find_last_oil():
        conn = DB.connect()
        cursor = cursor.execute("""SELECT * FROM track WHERE distance > 300 """)
        return cursor.fetchone()

    def save(time, lat, lon, speed, distance, oil=False):
        conn = DB.connect()
        cursor = conn.cursor()
        created_at = datetime.now()
        try:
            cursor.execute(
                """INSERT INTO track VALUES (?,?,?,?,?,?,?)""",
                (time, lat, lon, speed, distance, oil, created_at),
            )
            conn.commit()
        except Exception as ex:
            print(ex)  # TO-DO: Use logger
            return False
        finally:
            conn.close()

        return True
