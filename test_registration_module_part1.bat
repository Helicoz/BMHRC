@echo off

cd /d %~dp0

:: ======================================
:: Test Information
:: ======================================

set /p tester=Enter Tester Name:
set /p env=Enter Environment (QA/UAT/PROD):
set /p revisit_crn=Enter a CRN number with gender female and age above 18 and must be non admitted patient:
set /p abha_mobile=Enter Mobile Number for ABHA Verification:

call .venv\Scripts\activate

:: ======================================
:: Validate Fallback CRN
:: ======================================

if "%revisit_crn%"=="" (
    echo.
    echo ERROR: Fallback Revisit CRN cannot be empty.
    echo.
    pause
    exit /b 1
)

if "%abha_mobile%"=="" (
    echo.
    echo ERROR: ABHA mobile number cannot be empty.
    echo.
    pause
    exit /b 1
)

:: ======================================
:: Display Test Configuration
:: ======================================

echo.
echo ======================================
echo Test Configuration
echo ======================================
echo Tester       : %tester%
echo Environment  : %env%
echo Fallback CRN : %revisit_crn%
echo ABHA Mobile  : %abha_mobile%
echo ======================================
echo.

:: ======================================
:: Report Folder
:: ======================================

set REPORT_FOLDER=Reports\patient_registration_flow_part1

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

set REPORT_FILE=%REPORT_FOLDER%\patient_registration_flow_part1_%timestamp%.html

:: ======================================
:: RUN PYTEST
:: ======================================

pytest ^
-m patient_registration_flow_part1 ^
-v ^
--html="%REPORT_FILE%" ^
--self-contained-html ^
--tester="%tester%" ^
--env="%env%" ^
--revisit-crn="%revisit_crn%" ^
--abha-mobile="%abha_mobile%"

:: ======================================
:: TEST COMPLETE
:: ======================================

echo.
echo ======================================
echo Test execution completed.
echo ======================================
echo Report:
echo %REPORT_FILE%
echo ======================================

pause