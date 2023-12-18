import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)
common_module_dir = os.path.join(script_dir, 'service')
sys.path.append(common_module_dir)
import platform

def main():
    if platform.system() == 'Windows':
        import servicemanager
        import win32serviceutil
        from service.window_service import FileSorterWatcherWindowService
        if len(sys.argv) == 1:
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(FileSorterWatcherWindowService)
            servicemanager.StartServiceCtrlDispatcher()
        else:
            win32serviceutil.HandleCommandLine(FileSorterWatcherWindowService)
    elif platform.system() == 'Darwin':
        import plistlib
        import os
        #TODO: review MacOS install
        plist_data = {
            'Label': 'com.filesorter.watcherservice',
            'ProgramArguments': ['/usr/bin/python3', 'main.py'],
            'RunAtLoad': True,
            'KeepAlive': True,
        }

        plist_filename = 'com.filesorter.watcherservice'
        with open(plist_filename, 'wb') as plist_file:
            plistlib.dump(plist_data, plist_file)

        os.system(f'launchctl load {plist_filename}')

    else:
        print("Unsupported platform")

if __name__ == '__main__':
    main()
