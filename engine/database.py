import sqlite3
import os
import logging

logger = logging.getLogger("Priorization_Pipeline")

def save_to_sql(assets_dicts, db_path):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
        
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS asset_history (
                    id TEXT,
                    score REAL,
                    x REAL,
                    y REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                 )
            """)

            for asset in assets_dicts:
                cursor.execute("""
                    INSERT INTO asset_history (id, score, x, y)
                    VALUES (?,?,?,?)
                """, (
                    asset["id"],
                    asset["score"],
                    asset["geometry"]["x"],
                    asset["geometry"]["y"]
                ))

            conn.commit()
            logging.info(f"Successfully saved {len(assets_dicts)} records to SQLite database")
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")

    finally:
        if conn:
            conn.close()
            logging.debug("Database connection closed.")
