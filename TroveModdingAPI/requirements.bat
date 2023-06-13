@ECHO OFF
call .\venv\Scripts\activate.bat
echo Updating PIP!
python -m pip install -U pip
echo Updated PIP!
echo Installing requirements.txt
python -m pip install -r requirements.txt -U --no-cache-dir --force-reinstall
echo Installed requirements.txt
PAUSE