import sqlite3
from config import TARGET_SECTORS

DB_NAME = "victims.db"


def filter_victims():
  keywords = [kw.lower() for kw in TARGET_SECTORS]
  print(f"[*] Loaded keywords: {keywords}")

  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()

  cursor.execute(
      "SELECT id, victim, group_name, sector, domain FROM victims"
  )
  rows = cursor.fetchall()

  matched_count = 0
  print("\n[+] Matching victims in target sectors:")
  print("-" * 60)

  for row in rows:
    record_id, victim, group_name, sector, domain = row
    text_to_check = f"{str(victim)} {str(sector)} {str(domain)}".lower()

    matched_kw = [kw for kw in keywords if kw in text_to_check]

    if matched_kw:
      matched_count += 1
      print(
          f"Found: {victim} | Group: {group_name} | Sector: {sector} | Matched"
          f" KW: {matched_kw}"
      )

  print("-" * 60)
  print(f"[+] Total matching target sector victims found: {matched_count}")
  conn.close()


if __name__ == "__main__":
  filter_victims()