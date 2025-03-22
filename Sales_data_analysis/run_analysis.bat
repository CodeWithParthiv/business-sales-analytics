@echo off
echo Retail Sales Data Analysis
echo ========================
echo.
echo Choose an analysis to run:
echo 1. Basic Sales Analysis
echo 2. Advanced Sales Analysis
echo 3. Run Both Analyses
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Running Basic Sales Analysis...
    python simple_dashboard.py
    pause
) else if "%choice%"=="2" (
    echo.
    echo Running Advanced Sales Analysis...
    python simple_advanced_analysis.py
    pause
) else if "%choice%"=="3" (
    echo.
    echo Running Basic Sales Analysis...
    python simple_dashboard.py
    echo.
    echo Running Advanced Sales Analysis...
    python simple_advanced_analysis.py
    pause
) else if "%choice%"=="4" (
    echo Exiting...
) else (
    echo Invalid choice. Please try again.
    pause
) 