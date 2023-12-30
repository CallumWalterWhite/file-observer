# Define variables
$pythonExe = "python.exe"
$pyInstallerArgs = "pyinstaller -F --hidden-import=win32timezone -n filesorterservice ..\service\main.py"
$exePath = "..\dist\filesorterservice.exe"
& $pythonExe $pyInstallerArgs
& $exePath install
& $exePath start