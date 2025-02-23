## SMTP configuration in .env file
[Instruction](https://itsupport.umd.edu/itsupport?id=kb_article_view&sysparm_article=KB0015112) how to create an app password for gmail.
</br></br></br>

## Run the Python script in a terminal
1. Open a terminal and navigate to the target directory (set your USER_NAME):
   ```
   cd /home/USER_NAME/Desktop/AutoSpeedTest
   ```
2. Run the Python script:
   ```
   python3 main.py
   ```
</br>

## Creating a .desktop executable file for Ubuntu
1. Create the .desktop file on the Desktop:
   ```
   nano ~/Desktop/AutoSpeedTest.desktop
   ```
2. Add the following content (set your USER_NAME):
   ```
   [Desktop Entry]
   Version=1.0
   Type=Application
   Name=AutoSpeedTest
   Comment=Automatic speed test
   Exec=gnome-terminal -- bash -c "cd /home/USER_NAME/Desktop/AutoSpeedTest && python3 main.py; exec bash"
   Icon=utilities-terminal
   Terminal=true
   Categories=Utility;Network;
   ```
   * `Exec=` ensures the script runs in a terminal.
   * `Icon=` uses the default terminal icon. You can replace it with a custom one.
   * `Terminal=true` ensures the script runs in a visible terminal window.\
   After pasting, save the file:
   * Press `Ctrl + X`.
   * Press `Y` to confirm saving.
   * Press `Enter` to save and exit.
4. Grant execution permissions:
   ```
   chmod 755 ~/Desktop/AutoSpeedTest.desktop
   ```
   If you give too broad permissions (e.g. `+x`), GNOME may block the application.
5. Mark the file as trusted:
   ```
   gio set ~/Desktop/AutoSpeedTest.desktop metadata::trusted true
   ```
</br>

## Creating a .bin executable file for Ubuntu
**This is the best solution - we will be able to run our application using a `.bin` file on any Linux computer.**
1. Install `pipx`:
   ```
   sudo apt install pipx
   ```
   `pipx` is a package manager that allows you to install Python applications in isolated environments. It ensures that tools like `pyinstaller` do not interfere with system-wide packages.
2. Add pipx to your system's PATH, ensuring that installed applications (like PyInstaller) can be used from anywhere:
   ```
   pipx ensurepath
   ```
3. Install `PyInstaller`:
   ```
   pipx install pyinstaller
   ```
4. Add the necessary dependencies to the PyInstaller environment:
   ```
   pipx inject pyinstaller selenium python-dotenv
   ```
5. Navigate to the project directory, e.g.:
   ```
   cd ./Desktop/AutoSpeedTest
   ```
6. Generate the `.spec` file:
   ```
   pyinstaller --onefile --name=AutoSpeedTest main.py
   ```
7. Open `AutoSpeedTest.spec`:
   ```
   nano AutoSpeedTest.spec
   ```
   And edit `hiddenimports` in `a = Analysis(`:
   ```
   hiddenimports=[
    'selenium',
    'selenium.common',
    'selenium.webdriver',
    'selenium.webdriver.common',
    'selenium.webdriver.firefox.service',
    'selenium.webdriver.firefox.webdriver',
    'dotenv'
   ],
   ```
   Save the file:
   * Press `Ctrl + X`.
   * Press `Y` to confirm saving.
   * Press `Enter` to save and exit.
8. ...
