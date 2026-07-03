import sqlite3
import logging
from contextlib import closing

logger = logging.getLogger("Prioritization_Pipeline")


def save_to_sql(assets_dicts, db_path):
    try:
        with closing(sqlite3.connect(db_path)) as conn:
            with conn:  # Transaktion: auto-commit bei Erfolg, rollback bei Fehler
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
                        VALUES (?, ?, ?, ?)
                    """, (
                        asset["id"],
                        asset["score"],
                        asset["geometry"]["x"],
                        asset["geometry"]["y"]
                    ))

        logger.info(f"Successfully saved {len(assets_dicts)} records to SQLite database")
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
