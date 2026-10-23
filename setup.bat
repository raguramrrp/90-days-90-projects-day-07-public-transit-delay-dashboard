@echo off
setlocal enabledelayedexpansion

echo =====================================================================
echo  Public Transit Delay Analytics Dashboard - Windows Setup (Day 7)
echo =====================================================================

:: 1. Check Python installation
where py >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=py -3.12"
    py -3.12 --version >nul 2>&1
    if !ERRORLEVEL! neq 0 (
        set "PY_CMD=py -3"
    )
) else (
    where python >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        set "PY_CMD=python"
    ) else (
        echo [ERROR] Python 3.10+ was not found on your system PATH.
        echo Please install Python 3.10, 3.11, or 3.12 from https://www.python.org/
        pause
        exit /b 1
    )
)

echo [OK] Using Python launcher: %PY_CMD%

:: 2. Create virtual environment
if not exist ".venv\Scripts\python.exe" (
    echo [INFO] Creating isolated virtual environment in .venv...
    %PY_CMD% -m venv .venv
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created.
) else (
    echo [OK] Virtual environment already exists.
)

:: 3. Upgrade pip and install dependencies
echo [INFO] Installing required dependencies from requirements.txt...
.venv\Scripts\python.exe -m pip install --upgrade pip --quiet
.venv\Scripts\python.exe -m pip install -r requirements.txt --quiet
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo [OK] Python dependencies installed successfully.

:: 4. Setup environment variables
if not exist ".env" (
    echo [INFO] Creating .env from .env.example...
    copy ".env.example" ".env" >nul
    echo [OK] .env configuration file created.
) else (
    echo [OK] .env file already present.
)

:: 5. Create local directories
if not exist "data\raw" mkdir "data\raw"
if not exist "data\processed" mkdir "data\processed"
if not exist "data\powerbi_export" mkdir "data\powerbi_export"
if not exist "screenshots" mkdir "screenshots"

:: 6. Seed database and run ETL
echo [INFO] Running Transit ETL Pipeline to seed database...
.venv\Scripts\python.exe src\etl.py
if %ERRORLEVEL% neq 0 (
    echo [ERROR] ETL data pipeline failed to initialize database.
    pause
    exit /b 1
)
echo [OK] Database seeded and initialized with transit observations.

:: 7. Export Power BI Star-Schema Datasets
echo [INFO] Generating Power BI dimensional models and DAX measures...
.venv\Scripts\python.exe src\powerbi_export.py
echo [OK] Power BI export datasets created.

echo =====================================================================
echo  [SUCCESS] Setup Completed! You can now start the application:
echo  Run: run.bat
echo  Test: test.bat
echo =====================================================================
pause
