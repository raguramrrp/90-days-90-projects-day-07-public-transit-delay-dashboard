# Troubleshooting & FAQ

## 1. Common Windows Setup Issues

### Issue 1: `Python was not found on your system PATH`
- **Cause**: Python is installed but not added to system environment variables, or the Windows Python Launcher (`py`) is missing.
- **Resolution**:
  1. Open PowerShell and test if the Python launcher works:
     ```cmd
     py -3.12 --version
     ```
  2. If not found, download Python 3.12 or 3.11 from [python.org](https://www.python.org/) and check **"Add Python to PATH"** during installation.

### Issue 2: `setup.bat` fails during `pip install`
- **Cause**: Network timeout or permission restrictions on `.venv`.
- **Resolution**:
  1. Delete the existing `.venv` folder:
     ```cmd
     rmdir /s /q .venv
     ```
  2. Re-run `setup.bat`.
  3. Alternatively, install dependencies manually:
     ```cmd
     py -3.12 -m venv .venv
     .venv\Scripts\python.exe -m pip install -r requirements.txt
     ```

### Issue 3: Streamlit Port 8501 Already in Use
- **Cause**: Another local Streamlit app or process is occupying port 8501.
- **Resolution**:
  Launch the app on a different port:
  ```cmd
  .venv\Scripts\streamlit.exe run app.py --server.port=8502
  ```

---

## 2. Database & Data Issues

### Issue 4: Database shows 0 records on first run
- **Cause**: Initial ETL pipeline was bypassed or interrupted.
- **Resolution**:
  1. Click the **"🔄 Refresh Data"** button in the dashboard sidebar.
  2. Or run the ETL pipeline from the command line:
     ```cmd
     .venv\Scripts\python.exe src\etl.py
     ```

### Issue 5: How do I switch to PostgreSQL?
- **Resolution**:
  1. Create a PostgreSQL database (e.g. `transit_analytics`).
  2. Open `.env` and set `DATABASE_URL`:
     ```ini
     DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/transit_analytics
     ```
  3. Run the PostgreSQL DDL script located at `sql/postgres_setup.sql`.
  4. Run `setup.bat` or `python src/etl.py` to ingest data into PostgreSQL.

---

## 3. Power BI Integration Issues

### Issue 6: Power Query reports "File not found" for CSV files
- **Cause**: Power BI needs absolute file paths or matching relative folder paths.
- **Resolution**:
  1. In Power BI Desktop, open **Transform Data** -> **Data Source Settings**.
  2. Update the folder path to point directly to `<your-project-path>/data/powerbi_export/`.
  3. Click **Close & Apply**.
