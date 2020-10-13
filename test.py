import sys
import time
import logging
import shutil
import ntpath
import os
import glob
import subprocess

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import LoggingEventHandler

INPUT_QUEUE = 'Z:\\SW_IN\\'
PDF_DEST    = 'L:\\pdf_out\\'
PDF_ARCHIVE = 'L:\\pdf_out\\archive\\'
WATCH_SW    = 'L:\\SWDRAW~1'                                # l:/SW Drawings
WATCH_AC    = 'L:\\DRAWINGS'
WATCH_RS    = 'I:\\Research\\R51541\\Finished'
WATCH_PF    = 'H:\\Plot\\PDF'

WATCHED_FOLDERS = [
    { 'folder': 'L:\\SWDRAW~1',                   'types': ['SLDDRW'] },
    { 'folder': 'L:\\DRAWINGS',                   'types': ['DWG'] },
    { 'folder': 'I:\\Research\\R51541\\Finished', 'types': ['SLDDRW', 'DWG'] },
    { 'folder': 'H:\\Plot\\PDF',                  'types': ['PDF'] }
    ]

# *******************************************************************

class Logger(logging.Logger):
   def __init__(self):
       logging.Logger.__init__(self, 'watch_drawing_folders')

       formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
       #     Set level for the events to be logged
       self.root.setLevel(logging.NOTSET)
       #     Create handler for logging to console
       console = logging.StreamHandler()
       console.setLevel(0)
       console.setFormatter(formatter)
       self.addHandler(console)
       #     Create handler for logging to log file
       sLogFile = './log/watch_drawing_folders.log'
       fileHandler = logging.FileHandler(sLogFile)
       fileHandler.setFormatter(formatter)
       self.addHandler(fileHandler)

logger = Logger()

logger.info('==============[ watch_drawing_folders processor ]================')

# *******************************************************************

class HandleFiles(FileSystemEventHandler):
  def on_modified(self, event):
    logger.info(' detect DWG or SLDDRW drawing - ' + event.src_path)
    file_type = event.src_path[event.src_path.rfind('.'):].upper()
    xPos = event.src_path.rfind('\\')
    first_char = event.src_path[xPos + 1:xPos + 2]

    if first_char == '~':
      return None

    if file_type == '.SLDDRW' or file_type == '.DWG':
      time.sleep(2)
      shutil.copy(str(event.src_path), INPUT_QUEUE)
      logger.info(' copied - ' + event.src_path)

# *******************************************************************

class HandlePDFs(FileSystemEventHandler):
  def on_modified(self, event):
    logger.info(' - detect PDF drawing - ' + event.src_path)
    file_type = event.src_path[event.src_path.rfind('.'):].upper()
    xPos = event.src_path.rfind('\\')
    first_char = event.src_path[xPos + 1:xPos + 2]

    if first_char == '~':
      return None

    if file_type == '.PDF':
      #logger.info(' - ' + event.event_type, event.src_path + ' - type: ' + file_type)
      time.sleep(20)
      filename = str(os.path.basename(event.src_path))
      if os.path.exists(PDF_DEST + filename):
        # ************** backup PDF
        shutil.copy(PDF_DEST + filename, PDF_ARCHIVE + time.strftime('%Y-%m-%d_%H-%M') + '_' + filename)
        os.remove(PDF_DEST + filename)
        #shutil.move(PDF_DEST + filename, PDF_ARCHIVE + time.strftime('%Y-%m-%d_%H-%M') + '_' + filename)
        logger.info(' - backup - ' + PDF_ARCHIVE + time.strftime('%Y-%m-%d_%H-%M') + '_' + filename)

      # ************** copy PDF
      #shutil.copy(str(event.src_path), PDF_DEST)
      shutil.move(str(event.src_path), PDF_DEST)
      logger.info(' - moved - ' + PDF_DEST + filename)

# *******************************************************************

def check_for_waiting_files():
  '''
  Run this check whenever watcher is started or restarted.
  Check pdf_out folder for newest file
  Check drawing folders for drawing files newer than newest PDF
  Copy unprocessed drawings to generator INPUT_QUEUE
  '''

  logger.info(' - Checking for newest PDF file.  Please wait...')
  newest = max(glob.iglob(PDF_DEST + '\\*.pdf'), key=os.path.getmtime)
  logger.info(' - Newest PDF file:'.ljust(20) + newest[newest.rfind('\\') + 1:])
  logger.info(' - Updated: '.ljust(20) + time.strftime('%Y%m%d %H:%M', time.localtime(os.path.getmtime(newest))))
  newest_date = time.strftime('%Y%m%d', time.localtime(os.path.getmtime(newest)))
  newest_date_for = time.strftime('%m/%d/%Y', time.localtime(os.path.getmtime(newest)))
  newest_date_time = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(os.path.getmtime(newest)))

  for FOLDER in WATCHED_FOLDERS:
    cmd = 'forfiles /P ' + FOLDER['folder'] + ' /S /D +' + newest_date_for

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    logger.info(' - Missed files from ' + FOLDER['folder'] + ':')
    for line in p.stdout.readlines():
      file_name = line[:-2].translate(None, ''.join('"'))
      if any(type in file_name.upper() for type in FOLDER['types']):
        file_modified = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(os.path.getmtime(FOLDER['folder'] + '\\' + file_name)))
        if (file_modified > newest_date_time):
          logger.info(' - Processing - ' + file_name + ' - ' + file_modified)
          shutil.copy(FOLDER['folder'] + '\\' + file_name, INPUT_QUEUE)

# *******************************************************************

if __name__ == "__main__":
    logger.info(' - ************************ Start Watching ************************')
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    check_for_waiting_files()

    logger.info(' converter queue: ' + INPUT_QUEUE)
    event_handler = HandleFiles()
    observer_sw   = Observer()
    observer_sw.schedule(event_handler, WATCH_SW, recursive=False)
    logger.info('        watching: ' + WATCH_SW)
    observer_sw.start()

    observer_ac   = Observer()
    observer_ac.schedule(event_handler, WATCH_AC, recursive=False)
    logger.info('        watching: ' + WATCH_AC)
    observer_ac.start()

    observer_rs   = Observer()
    observer_rs.schedule(event_handler, WATCH_RS, recursive=False)
    logger.info('        watching: ' + WATCH_RS)
    observer_rs.start()

    pdf_handler = HandlePDFs()
    observer_pf = Observer()
    observer_pf.schedule(pdf_handler, WATCH_PF, recursive=False)
    logger.info('        watching: ' + WATCH_PF)
    observer_pf.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer_sw.stop()
        observer_ac.stop()
        observer_rs.stop()
        observer_pf.stop()

    observer_sw.join()
    observer_ac.join()
    observer_rs.join()
    observer_pf.join()
