from datetime import datetime
import sqlite3
import requests

DB_NAME = "victims.db"
API_URL = "https://api.ransomware.live/recentvictims"


def init_db():
  """Initializes the SQLite database and victims table if it doesn't exist."""
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS victims (
            id TEXT PRIMARY KEY,
            victim TEXT,
            group_name TEXT,
            discovered TEXT,
            country TEXT,
            sector TEXT,
            domain TEXT,
            first_seen_by_tool TEXT
        )
    """)
  conn.commit()
  conn.close()


def fetch_recent_victims():
  """Fetches recent victim data from the ransomware.live API."""
  print(f"[*] Fetching data from {API_URL}...")
  try:
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()
    return response.json()
  except requests.exceptions.RequestException as e:
    print(f"[!] Error fetching data: {e}")
    return []


def save_victims(victims):
  """Normalizes and inserts victims into the SQLite database, ignoring duplicates."""
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()

  new_count = 0
  now = datetime.utcnow().isoformat()

  for item in victims:
    victim_name = item.get("post_title") or item.get("victim", "Unknown")
    group_name = item.get("gang") or item.get("group_name", "Unknown")
    discovered_date = item.get("discovered") or item.get("date", "Unknown")
    country = item.get("country", "Unknown")
    sector = item.get("sector", "Unknown")
    domain = item.get("domain", "")

    # Create a unique composite primary key to prevent duplicate entries
    record_id = f"{group_name}_{victim_name}_{discovered_date}".strip().lower()
    record_id = "".join(record_id.split())

    try:
      cursor.execute(
          """
                INSERT OR IGNORE INTO victims 
                (id, victim, group_name, discovered, country, sector, domain, first_seen_by_tool)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
          (
              record_id,
              victim_name,
              group_name,
              discovered_date,
              country,
              sector,
              domain,
              now,
          ),
      )
      if cursor.rowcount > 0:
        new_count += 1
    except sqlite3.Error as e:
      print(f"[!] Database error: {e}")

  conn.commit()
  conn.close()
  print(f"[+] Done! Added {new_count} new unique victims to {DB_NAME}.")


if __name__ == "__main__":
  print("[*] Starting Ransomware Leak Tracker Collector...")
  init_db()
  data = fetch_recent_victims()
  if data:
    save_victims(data)
  else:
    print("[!] No data retrieved.")