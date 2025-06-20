# 🧾 log-monitoring-app

A lightweight Python application that monitors log files calculates the duration of each job, and classifies them based on processing time. 
It reports **warnings** and **errors** when execution thresholds are exceeded.

---

## 📌 Features

- Parses a CSV log file with lines in the format:
- Matches `START` and `END` events for each PID.
- Calculates job durations.
- Classifies jobs as:
- ✅ OK (≤ 5 minutes)
- ⚠️ WARNING (> 5 minutes)
- ❌ ERROR (> 10 minutes)
- Reports incomplete jobs (missing START or END).
- Clear, readable output in terminal or logs.

---

## Environment Setup

1. **Clone the repo:**

   ```bash
   git clone https://github.com/VasilescuO/log-monitoring-app.git
   ```
2. **Install [uv](https://github.com/astral-sh/uv) if you don't have it:**
   ```sh
   pip install uv
   ```
3. **Setup virtual environment:**
   ```sh
   uv venv
   # activate virtual environment
   source .venv/bin/activate
   ```

4. **Install dependencies:**
   ```sh
    uv pip install -r pyproject.toml
   ```

5. **Run tests**
   ```sh
   pytest tests/test_parser.py
   ``` 
6. **Run the application:**
   ```sh
    python3 main.py
   ```