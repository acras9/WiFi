@echo off
echo Creating Python virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing required packages...
pip install -r requirements.txt

echo Setup completed!
echo To activate the virtual environment, use: venv\Scripts\activate
echo To run the server, use: python main.py
pause
