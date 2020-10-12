# Python-DWG_to_PDF
Requirements
 - Create a python script to look at multiple directories that contain DWG file (specified directories as a variable... ex c:\DWGFiles && c:\Autocade && c:\somewhereelse)
 - On the initial run we need to convert EVERY DWG to a PDF
 - on each run after the initial run we only want to look for files that are new or that have changed (one way to do this is to record the timestamp of the last runtime of the script. If we check it each time we run the conversion we should then look for files that are the same time or newer than the last runtime)
 - The output should be the same.filename.dwg converted to same.filename.pdf
 - The Converter will use IrfanView installed on the same machine the script runs from
 - the output file should live inside a different folder of the scripts choice (ex. c:\PDFout\*)
 
 
