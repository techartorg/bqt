echo off
set "bln_ver=3.2"
set "bln_dir=C:\Program Files\Blender Foundation\Blender %bln_ver%"
set "bln_exe=%bln_dir%\blender.exe"
set "bln_py=%bln_dir%\%bln_ver%\python\bin\python.exe"

call "%bln_py%" -m venv env
call "%~dp0env\Scripts\activate"

SET PIP_DISABLE_PIP_VERSION_CHECK=1
:: dev requirements only for ease of use in ide
call python -m pip install -r dev-requirements.txt
call python -m pip install -r requirements.txt
:: call python -m pip install %~dp0 --use-feature=in-tree-build

set "BLENDER_USER_SCRIPTS=%~dp0"
call "%bln_exe%"
