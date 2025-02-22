@echo off
setlocal enableDelayedExpansion
(
  python3 -m pip install -r requirements.txt
  set "errorlevel=1"
  set "errorlevel="
  if !errorlevel! neq 0 (python -m pip install -r requirements.txt)
)