@echo off
cd /d "%~dp0"

"%~dp0venv\Scripts\python.exe" -m pytest --alluredir=allure-results --clean-alluredir
set "pytest_exit=%ERRORLEVEL%"
if %pytest_exit% GEQ 2 exit /b %pytest_exit%

call allure.cmd generate allure-results --output allure-report
if errorlevel 1 exit /b %ERRORLEVEL%

call allure.cmd open .\allure-report\awesome
exit /b %pytest_exit%