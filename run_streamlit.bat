@echo off
title Multimodal Construction Intelligence Platform
echo =====================================================================
echo  MULTIMODAL CONSTRUCTION INTELLIGENCE PLATFORM (CAPSTONE PROJECT 1)
echo  Platform ID: 6ac4c98d1dcde6d7857c1642
echo =====================================================================
echo.
echo Starting Streamlit Server...
echo.

python -m streamlit run app.py --server.port=8501

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to launch Streamlit.
    echo Please make sure dependencies are installed: pip install -r requirements.txt
    pause
)
