:CHECK_L
echo.
echo  Z: drive is mapped
if exist L:\Drawings goto WATCH

net use L: \\engserver1\files$

:WATCH
echo.
echo  L: drive is mapped
echo.

echo %DATE% - %TIME% - ********* Starting eDrawings PDF Generator process ******************
:START_PDF_GENERATOR

call C:\var\hg\SendPlot-System\source\watchdog\eDrawingsPDFGenerator.accdb
echo %DATE% - %TIME% - ********* Time out waiting for eDrawings PDF Generator process restarting... ******************

goto START_PDF_GENERATOR
