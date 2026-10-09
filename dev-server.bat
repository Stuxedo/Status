@echo off
setlocal
REM Status - Local dev server (Windows)
REM Usage: dev-server.bat [--no-dev-mode] [port]
REM   port            default: 8000
REM   --no-dev-mode   render the status page exactly as production would
REM
REM Generates 90 days of example data for the monitors in .githup.yml, builds
REM the GitHup status page into .dev\public, with its legal pages, 404 and sitemap,
REM and serves it with python -m http.server, just like
REM https://status.stuxedo.net.
REM
REM GitHup itself is found at %GITHUP_PATH%, else ..\GitHup or ..\..\Stux.Group\GitHup (a local checkout),
REM else it is cloned into .dev\GitHup.
REM the status page, its legal pages and 404 show GitHup's DEV MODE banner.

set "DIR=%~dp0"
set "PORT=8000"
set "DEV_MODE=1"

:args
if "%~1"=="" goto run
if /i "%~1"=="--no-dev-mode" (
    set "DEV_MODE=0"
) else (
    set "PORT=%~1"
)
shift
goto args

:run
cd /d "%DIR%"
set "GITHUP=%GITHUP_PATH%"
if not "%GITHUP%"=="" goto found
if exist "%DIR%..\GitHup\githup\__init__.py" (
    set "GITHUP=%DIR%..\GitHup"
    goto found
)
if exist "%DIR%..\..\Stux.Group\GitHup\githup\__init__.py" (
    set "GITHUP=%DIR%..\..\Stux.Group\GitHup"
    goto found
)
set "GITHUP=%DIR%.dev\GitHup"
if not exist "%GITHUP%" git clone --depth 1 https://github.com/StuxGroup/GitHup.git "%GITHUP%" || exit /b 1

:found
set "PYTHONPATH=%GITHUP%"
set "PYTHONDONTWRITEBYTECODE=1"

REM GitHup empties its output folder, so the status page is built first.
python -m githup demo --config .githup.yml --data-dir .dev/data || exit /b 1
python -m githup site --config .githup.yml --data-dir .dev/data --incidents-file .dev/data/incidents.json --out .dev/public --no-deploy || exit /b 1

if "%DEV_MODE%"=="1" (
    echo Stuxedo Status ^(DEV_MODE=1^) at http://127.0.0.1:%PORT%/
) else (
    echo Stuxedo Status ^(production rendering^) at http://127.0.0.1:%PORT%/
)
python -m http.server %PORT% --bind 127.0.0.1 --directory .dev/public
