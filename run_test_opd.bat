@echo off

cd /d %~dp0

set /p tester=Enter Tester Name:
set /p env=Enter Environment (QA/UAT/PROD):

call .venv\Scripts\activate

:: ======================================
:: Report Folder
:: ======================================
set REPORT_FOLDER=Reports\OPD

if not exist "%REPORT_FOLDER%" (
    mkdir "%REPORT_FOLDER%"
)

:: ======================================
:: Timestamp
:: ======================================
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format \"yyyy-MM-dd_hh-mm-ss_tt\""') do set timestamp=%%i

:: ======================================
:: Report Name
:: ======================================
set REPORT_FILE=%REPORT_FOLDER%\opd_flow_%timestamp%.html

pytest ^
-m opd_flow ^
-v ^
--html="%REPORT_FILE%" ^
--self-contained-html ^
--tester="%tester%" ^
--env="%env%"

pause