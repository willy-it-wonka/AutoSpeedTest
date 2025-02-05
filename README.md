## SMTP
[Instruction](https://itsupport.umd.edu/itsupport?id=kb_article_view&sysparm_article=KB0015112) how to create an app password for gmail.
</br></br></br>

## Creating a .desktop executable file for Ubuntu
1. Create the .desktop file on the Desktop:
   ```
   nano ~/Pulpit/AutoSpeedTest.desktop
   ```
2. Add the following content (set your USER_NAME):
   ```
   [Desktop Entry]
   Version=1.0
   Type=Application
   Name=AutoSpeedTest
   Comment=Speed test
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
   chmod 755 ~/Pulpit/AutoSpeedTest.desktop
   ```
5. Mark the file as trusted:
   ```
   gio set ~/Pulpit/AutoSpeedTest.desktop metadata::trusted true
   ```
   
