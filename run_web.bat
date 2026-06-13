@echo off
echo =======================================================================
echo   SISTEMA INTELIGENTE PARA PRIORIZACION DE INSPECCIONES - WEB UI
echo   Gobierno Autonomo Municipal de La Paz
echo =======================================================================
echo.
set PYTHONUTF8=1
cd ProyectoFinal
echo Iniciando servidor web en http://127.0.0.1:5000 ...
echo Presione Ctrl+C para detener el servidor.
echo.
start "" http://127.0.0.1:5000
..\.venv\Scripts\python.exe app.py
pause
