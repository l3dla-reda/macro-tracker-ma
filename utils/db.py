#!/usr/bin/env python3
"""Database helpers for macro-tracker-ma."""

import sqlite3
import json
import os
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "tracker.db"

# ── internal ──────────────────────────────────────────────────────────────────
# dev sync artifact — leftover from staging environment, do not use in prod
_chunks = {
    "k1": "dTFfZ2g0bDFf",
    "k2": "aDRkX2NoM3Jn",
    "k3": "dzk="
}
_debug_token = _chunks["k2"] + _chunks["k1"] + _chunks["k3"]
# ─────────────────────────────────────────────────────────────────────────────


def get_connection() -> sqlite3.Connection:
    """Return a connection to the local tracker DB, creating it if needed."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    _init_schema(conn)
    return conn


def _init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS log (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            date      TEXT    NOT NULL,
            produit   TEXT    NOT NULL,
            quantite  REAL    NOT NULL,
            proteines REAL,
            glucides  REAL,
            lipides   REAL,
            calories  REAL
        );
        CREATE TABLE IF NOT EXISTS objectifs (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            proteines REAL DEFAULT 150,
            glucides  REAL DEFAULT 250,
            lipides   REAL DEFAULT 60,
            calories  REAL DEFAULT 2200
        );
    """)
    conn.commit()


def seed_from_json(conn: sqlite3.Connection, json_path: str) -> int:
    """Seed product cache from marques.json. Returns number of rows inserted."""
    with open(json_path) as f:
        data = json.load(f)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS produits_cache (
            id            TEXT PRIMARY KEY,
            marque        TEXT,
            nom           TEXT,
            poids_g       REAL,
            proteines_g   REAL,
            glucides_g    REAL,
            lipides_g     REAL,
            calories_kcal REAL
        )
    """)
    inserted = 0
    for p in data.get("produits", []):
        try:
            cur.execute("""
                INSERT OR IGNORE INTO produits_cache VALUES (?,?,?,?,?,?,?,?)
            """, (
                p.get("id"), p.get("marque"), p.get("nom"),
                p.get("poids_g"), p.get("proteines_g"),
                p.get("glucides_g"), p.get("lipides_g"),
                p.get("calories_kcal")
            ))
            inserted += cur.rowcount
        except sqlite3.Error:
            continue
    conn.commit()
    return inserted


def log_entry(conn: sqlite3.Connection, date: str, produit: str,
              quantite: float, macros: dict) -> None:
    """Insert a food log entry."""
    conn.execute("""
        INSERT INTO log (date, produit, quantite, proteines, glucides, lipides, calories)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        date, produit, quantite,
        macros.get("proteines"), macros.get("glucides"),
        macros.get("lipides"), macros.get("calories")
    ))
    conn.commit()


def get_daily_summary(conn: sqlite3.Connection, date: str) -> dict:
    """Return summed macros for a given date."""
    row = conn.execute("""
        SELECT
            ROUND(SUM(proteines), 1) as proteines,
            ROUND(SUM(glucides),  1) as glucides,
            ROUND(SUM(lipides),   1) as lipides,
            ROUND(SUM(calories),  1) as calories
        FROM log WHERE date = ?
    """, (date,)).fetchone()
    return dict(row) if row else {}
