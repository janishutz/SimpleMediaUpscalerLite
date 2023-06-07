curl -o ./pythonInstaller.exe https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe

wine pythonInstaller.exe

wine python -m pip install pyinstaller

printf '\n\n==> Done installing python for windows\n\n'