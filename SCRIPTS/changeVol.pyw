try:

    from sys import argv
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from ctypes import cast, POINTER

    COMMAND = argv[1]

    device = AudioUtilities.GetSpeakers()
    interface = device.Activate(IAudioEndpointVolume._iid_, 7, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    if COMMAND == 'getvol':
        with open('RESULT.txt', 'w') as f:
            f.write(str(int(volume.GetMasterVolumeLevelScalar() * 100)))

    if COMMAND == 'setvol':
        try:
            volume.SetMasterVolumeLevelScalar(int(argv[2]) / 100, None)
            with open('RESULT.txt', 'w') as f:
                f.write(f'VOLUME SET TO {argv[2]}')
        except Exception as e:
            print(e)
            with open('RESULT.txt', 'w') as f:
                f.write('FAILED TO CHANGE VOLUME!')

    if COMMAND == 'mute':
        try:
            volume.SetMute(1, None)
            with open('RESULT.txt', 'w') as f:
                f.write(f'MUTE SET')
        except:
            with open('RESULT.txt', 'w') as f:
                f.write('FAILED TO MUTE!')

    if COMMAND == 'unmute':
        try:
            volume.SetMute(0, None)
            with open('RESULT.txt', 'w') as f:
                f.write(f'UNMUTE SET')
        except:
            with open('RESULT.txt', 'w') as f:
                f.write('FAILED TO UNMUTE!')

except:

    with open('RESULT.txt', 'w') as f:
        f.write(f'FAILED TO RUN! ENSURE YOU CHOOSE A FUNCTION!')