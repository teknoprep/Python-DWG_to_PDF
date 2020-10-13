# Python-DWG_to_PDF
Requirements
 - Create a python script to look at multiple directories that contain DWG file (specified directories as a variable... ex c:\DWGFiles && c:\Autocade && c:\somewhereelse)
 - On the initial run we need to convert EVERY DWG to a PDF
 - on each run after the initial run we only want to look for files that are new or that have changed (one way to do this is to record the timestamp of the last runtime of the script. If we check it each time we run the conversion we should then look for files that are the same time or newer than the last runtime)
 - The output should be the same.filename.dwg converted to same.filename.pdf
 - The Converter will use IrfanView or something similar installed on the same machine the script runs from
 - the output file should live inside a different folder of the scripts choice (ex. c:\PDFout\*)
 

 Installing
---------------------------
1. Download <a href="https://github.com/FreeCAD/FreeCAD/releases">FreeCAD</a> and extract it.
2. Add paths lib and bin of FreeCAD into system path.
3. Donwload <a href="https://www.opendesign.com/guestfiles/oda_file_converter">ODAFileConverter</a> and install it.
4. Add path of ODAFileConverter into system path.
5. Install Python 3.8
6. Clone this project.
7. Run pip install -r requirements.txt
8. Copy "Lib\site-packages\dotenv" folder of python folder to "\bin\Lib\site-packages" of FreeCAD folder


Run
-------------------------------
1. Set SEARCH_FOLDERS(input folders with .dwg files) and RESULTS_FOLDER(output folder where .pdf files will be saved) in .env file .
2. Run Command Prompt
3. Move to bin folder of FreeCAD folder.
4. Run following command as:
    freecad <path of project>\app.py
 
