@echo off
if exist Z:\SW_IN goto CHECK_L

REM :: net use Z: \\is401\Converter-Z$
REM :: net use Z: \\SENDPLOTSERVER1\Converter-Z$
REM subst Z: C:\var\work

:CHECK_L
echo.
echo  Z: drive is mapped
if exist L:\Drawings goto WATCH

net use L: \\engserver1\files$

:WATCH
echo.
echo  L: drive is mapped
:START_WATCHING
echo.
echo  Starting watch %DATE% %TIME%
echo.
python watch_drawings_folder.py
echo.
echo  Restarting...
