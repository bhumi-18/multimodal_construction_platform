# PowerShell Launcher for Multimodal Construction Intelligence Platform
Write-Host "=====================================================================" -ForegroundColor Amber
Write-Host " MULTIMODAL CONSTRUCTION INTELLIGENCE PLATFORM (CAPSTONE PROJECT 1)" -ForegroundColor Yellow
Write-Host " Platform ID: 6ac4c98d1dcde6d7857c1642" -ForegroundColor Gray
Write-Host "=====================================================================" -ForegroundColor Amber

Write-Host "`nLaunching Streamlit application on http://localhost:8501...`n" -ForegroundColor Cyan
python -m streamlit run app.py --server.port=8501
