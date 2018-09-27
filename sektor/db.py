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
                speed INT, distance INT, oil BOOLEAN, created_at DATETIME)

                CREATE TABLE IF NOT EXISTS km_for_oil (id INT AUTO_INCREMENT, 
                counter INTEGER)
                """
            )
            conn.commit()
        finally:
            conn.close()
        return True

    def update_km_for_oil(distance):
        conn = DB.connect()
        cursor = conn.cursor()

        try:
            result = cursor.execute("""
                UPDATE counter set 
            """).fetchone()
            return result[0] if result else False
        except Exception as ex:
            print("Exception: ", ex)
            return False

    def get_last_oil_counter():
        conn = DB.connect()
        cursor = conn.cursor()

        try:
            result = cursor.execute("""
                SELECT counter FROM km_for_oil
            """).fetchone()
            return result[0] if result else False
        except Exception as ex:
            print("Exception: ", ex)
            return False

    def find_last_position():
        conn = DB.connect()
        cursor = conn.cursor()
        try:
            result = cursor.execute("""
                SELECT
                    track. `time`,
                    track.lat,
                    track.lon,
                    track.speed,
                    track.distance,
                    track.oil
                FROM
                    track
                ORDER BY
                    created_at DESC
                LIMIT 1
            """).fetchone()

            return result if result else False
        except Exception as ex:
            print("Exception on DB.find_last_position()")
            print("Exception: ", ex)
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
            print("Exception on DB.save()")
            print("Exception: ", ex)  # TO-DO: Use logger
            return False
        finally:
            conn.close()

        return True
