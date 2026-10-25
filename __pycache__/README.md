# Ransomware Leak-Site Tracker

An automated Cyber Threat Intelligence (CTI) pipeline that scrapes public ransomware extortion data, normalizes records into a local SQLite database, filters targets by critical industrial and semiconductor sectors, and generates executive weekly threat briefings with data visualizations.

---

## 🚀 The Problem & Objective
Security teams and organizations within high-value manufacturing and semiconductor sectors need near real-time visibility into active extortion groups targeting their supply chain. This project automates OSINT collection from public leak-site aggregators to track adversary activity without relying on paid commercial feeds.

---

## 🛠️ Architecture & Approach
1. **Data Collection (`collect.py`):** Pulls raw JSON payloads from public aggregator endpoints (`ransomware.live`), normalizes fields, and securely upserts records into a local SQLite database (`victims.db`) using a composite primary key (`group_name + victim + discovered date`) to eliminate duplicates.
2. **Sector Filtering (`filter.py` & `config.py`):** Applies keyword arrays (`semiconductor`, `chip`, `fab`, `manufacturing`, `industrial`, etc.) against victim names, sectors, and domains to isolate high-relevance supply chain threats.
3. **Automated Reporting (`report.py`):** Aggregates filtered data, computes weekly trends, generates Matplotlib visualizations, and compiles a structured executive Markdown summary (`weekly_report.md`).
4. **Cloud Automation (`.github/workflows/collect.yml`):** Uses GitHub Actions on a daily cron schedule to fetch fresh intel and automatically commit updated database states back to the repository.

---

## 📊 Sample Output & Visualizations

### Victims Over Time (Weekly Trend)
![Victims Per Week](victims_per_week.png)

### Top Threat Groups Targeting Target Sectors
![Top Groups](top_groups.png)

---

## ⚙️ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ds-cybersec/ransomware-leak-tracker.git](https://github.com/ds-cybersec/ransomware-leak-tracker.git)