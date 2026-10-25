from datetime import datetime
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
from config import TARGET_SECTORS

DB_NAME = "victims.db"


def generate_report():
  keywords = [kw.lower() for kw in TARGET_SECTORS]

  conn = sqlite3.connect(DB_NAME)
  query = "SELECT victim, group_name, discovered, country, sector, domain FROM victims"
  df = pd.read_sql(query, conn)
  conn.close()

  if df.empty:
    print("[!] No data found in database.")
    return

  # Normalize columns and filter by target keywords
  df["text_to_check"] = (
      df["victim"].astype(str)
      + " "
      + df["sector"].astype(str)
      + " "
      + df["domain"].astype(str)
  ).str.lower()

  # Filter rows matching any target keyword
  pattern = "|".join(keywords)
  filtered_df = df[df["text_to_check"].str.contains(pattern, na=False)].copy()

  print(f"[+] Total records in DB: {len(df)}")
  print(f"[+] Matching target sector records: {len(filtered_df)}")

  if filtered_df.empty:
    print(
        "[!] No matching sector victims found to generate charts. Try running"
        " the collector again later."
    )
    return

  # Clean up dates for weekly grouping
  filtered_df["discovered_date"] = pd.to_datetime(
      filtered_df["discovered"], errors="coerce"
  )
  filtered_df["week"] = (
      filtered_df["discovered_date"].dt.to_period("W").astype(str)
  )

  # 1. Chart: Victims per week
  weekly_counts = filtered_df.groupby("week").size()
  plt.figure(figsize=(8, 4))
  weekly_counts.plot(
      kind="line", marker="o", color="#1f77b4", title="Target Sector Victims Over Time"
  )
  plt.xlabel("Week")
  plt.ylabel("Victim Count")
  plt.grid(True)
  plt.tight_layout()
  plt.savefig("victims_per_week.png")
  plt.close()

  # 2. Chart: Top 10 groups targeting sectors
  top_groups = filtered_df["group_name"].value_counts().head(10)
  plt.figure(figsize=(10, 5))
  top_groups.plot(
      kind="bar", color="#ff7f0e", title="Top Threat Groups Against Target Sectors"
  )
  plt.xlabel("Threat Group")
  plt.ylabel("Victim Count")
  plt.xticks(rotation=45, ha="right")
  plt.tight_layout()
  plt.savefig("top_groups.png")
  plt.close()

  # Generate Markdown Report
  report_content = f"""# Ransomware Leak-Site Tracker: Weekly Threat Report
Generated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}

## Overview
This report highlights ransomware activity targeting semiconductor, manufacturing, and industrial sectors based on aggregated leak-site data[cite: 12].

- **Total Database Records:** {len(df)}
- **Target Sector Victims Identified:** {len(filtered_df)}

## Top Threat Groups Targeting Target Sectors
"""
  for group, count in top_groups.items():
    report_content += f"- **{group}**: {count} victim(s)\n"

  report_content += """
## Visualizations

### Victims Over Time (Weekly Trend)
![Victims Per Week](victims_per_week.png)

### Top Threat Groups
![Top Groups](top_groups.png)
"""

  with open("weekly_report.md", "w", encoding="utf-8") as f:
    f.write(report_content)

  print(
      "[+] Report generated successfully! Saved as weekly_report.md, along with"
      " charts."
  )


if __name__ == "__main__":
  generate_report()