# rushHourScraper

## Scraping server
The scraping server is available in the following folder
```
cd maps-python-scraper
```
Start a venv and activate it.
```
python -m venv venv
# In cmd.exe
venv\Scripts\activate.bat
# In PowerShell
venv\Scripts\Activate.ps1
# Linux / MacOS
$ source myvenv/bin/activate
```
Install the requirements
```
pip install -r requirements.txt
```
Run the server
```
uvicorn main:app --reload
```

## App

```
cd dashboard
npm run start
```
