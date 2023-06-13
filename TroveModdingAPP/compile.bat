@ECHO OFF
set name = "Trove Mod Manager"
set version = "0.1.000"
set author = "Sly"
"venv\Scripts\flet.exe" pack --icon="assets/favicon.ico" --add-data="assets;assets" --product-name="%name%" --file-description="%name%" --product-version="%version%" --file-version="%version%" --company-name="%author%" --copyright="%author%"  main.py>nul
PAUSE