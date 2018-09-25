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
                """CREATE TABLE IF NOT EXISTS track (            
                lat DOUBLE PRECISION, lat_cardinal VARCHAR(1), lon DOUBLE PRECISION, lon_cardinal VARCHAR(1),
                speed INT, distance INT, oil BOOLEAN, created_at DATETIME)"""
            )
            conn.commit()
        finally:
            conn.close()
        return True

    def find_last_oil():
        conn = DB.connect()
        cursor = cursor.execute("""SELECT * FROM track WHERE distance > 300 """)
        return cursor.fetchone()

    def save(lat, lat_cardinal, lon, lon_cardinal, speed, distance, oil=False):
        conn = DB.connect()
        cursor = conn.cursor()

        created_at = datetime.now()
        try:
            cursor.execute(
                """INSERT INTO track VALUES (?,?,?,?,?,?,?,?)""",
                (
                    lat,
                    lat_cardinal,
                    lon,
                    lon_cardinal,
                    speed,
                    distance,
                    oil,
                    created_at,
                ),
            )
            conn.commit()
        except Exception as ex:
            print(ex)  # TO-DO: Use logger
        finally:
            conn.close()

        return True
